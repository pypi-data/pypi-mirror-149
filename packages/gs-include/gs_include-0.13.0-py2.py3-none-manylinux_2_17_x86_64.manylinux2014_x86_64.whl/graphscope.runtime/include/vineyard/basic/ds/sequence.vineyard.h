#ifndef MODULES_BASIC_DS_SEQUENCE_VINEYARD_H
#define MODULES_BASIC_DS_SEQUENCE_VINEYARD_H

/** Copyright 2020-2021 Alibaba Group Holding Limited.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

#ifndef MODULES_BASIC_DS_SEQUENCE_MOD_H_
#define MODULES_BASIC_DS_SEQUENCE_MOD_H_

#include <memory>
#include <string>
#include <utility>
#include <vector>

#include "client/client.h"
#include "client/ds/blob.h"
#include "client/ds/core_types.h"
#include "client/ds/i_object.h"
#include "common/util/logging.h"
#include "common/util/uuid.h"

namespace vineyard {

#ifdef __GNUC__
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wattributes"
#endif

class SequenceBaseBuilder;

/**
 * @brief The sequence type in vineyard
 *
 */
class __attribute__((annotate("vineyard"))) Sequence : public Registered<Sequence> {
 
  public:
    static std::unique_ptr<Object> Create() __attribute__((used)) {
        return std::static_pointer_cast<Object>(
            std::unique_ptr<Sequence>{
                new Sequence()});
    }


  public:
    void Construct(const ObjectMeta& meta) override {
        std::string __type_name = type_name<Sequence>();
        VINEYARD_ASSERT(
            meta.GetTypeName() == __type_name,
            "Expect typename '" + __type_name + "', but got '" + meta.GetTypeName() + "'");
        this->meta_ = meta;
        this->id_ = meta.GetId();

        meta.GetKeyValue("size_", this->size_);
        for (size_t __idx = 0; __idx < meta.GetKeyValue<size_t>("__elements_-size"); ++__idx) {
            this->elements_.emplace_back(std::dynamic_pointer_cast<Object>(
                    meta.GetMember("__elements_-" + std::to_string(__idx))));
        }

        
    }

 private:
public:
  /**
   * @brief Get the size of the sequence, i.e., the number of elements it
   * contains.
   *
   * @return The size of the sequence.
   */
  size_t const Size() const { return this->size_; }

  /**
   * @brief Get the value at the given index.
   *
   * @param index The given index to get the value.
   */
  std::shared_ptr<Object> const At(size_t index) const {
    if (index >= size_) {
      LOG(ERROR) << "Sequence::at(): out of range: " << index;
      return nullptr;
    }
    return elements_[index];
  }

  /**
   * @brief Get the first element of the pair.
   *
   * @return The shared pointer to the first object.
   */
  std::shared_ptr<Object> const First() const { return this->At(0); }

  /**
   * @brief Get the second element of the pair.
   *
   * @return The shared pointer to the second object.
   */
  std::shared_ptr<Object> const Second() const { return this->At(1); }

  /**
   * @brief The iterator for the sequence object to iterate from the first to
   * the last element.
   *
   */
  class iterator
      : public std::iterator<
            std::bidirectional_iterator_tag, std::shared_ptr<Object>, size_t,
            const std::shared_ptr<Object>*, std::shared_ptr<Object>> {
    Sequence const* sequence_;
    size_t index_;

   public:
    explicit iterator(Sequence const* sequence, size_t index = 0)
        : sequence_(sequence), index_(index) {}
    iterator& operator++() {
      index_ += 1;
      return *this;
    }
    bool operator==(iterator other) const { return index_ == other.index_; }
    bool operator!=(iterator other) const { return index_ != other.index_; }
    reference operator*() const { return sequence_->At(index_); }
  };

  /**
   * @brief Get the beginning iterator.
   *
   * @return The beginning iterator.
   */
  const iterator begin() const { return iterator(this, 0); }

  /**
   * @brief Get the ending iterator.
   *
   * @return The ending iterator.
   */
  const iterator end() const { return iterator(this, size_); }

 private:
  __attribute__((annotate("shared"))) size_t size_;
  __attribute__((annotate("shared"))) Tuple<std::shared_ptr<Object>> elements_;

  friend class Client;
  friend class SequenceBaseBuilder;
};

#ifdef __GNUC__
#pragma GCC diagnostic pop
#endif

}  // namespace vineyard

#endif  // MODULES_BASIC_DS_SEQUENCE_MOD_H_

namespace vineyard {


class SequenceBaseBuilder: public ObjectBuilder {
  public:
    

    explicit SequenceBaseBuilder(Client &client) {}

    explicit SequenceBaseBuilder(
            Sequence const &__value) {
        this->set_size_(__value.size_);
        for (auto const &__elements__item: __value.elements_) {
            this->add_elements_(__elements__item);
        }
    }

    explicit SequenceBaseBuilder(
            std::shared_ptr<Sequence> const & __value):
        SequenceBaseBuilder(*__value) {
    }

    ObjectMeta &ValueMetaRef(std::shared_ptr<Sequence> &__value) {
        return __value->meta_;
    }

    std::shared_ptr<Object> _Seal(Client &client) override {
        // ensure the builder hasn't been sealed yet.
        ENSURE_NOT_SEALED(this);

        VINEYARD_CHECK_OK(this->Build(client));
        auto __value = std::make_shared<Sequence>();

        return this->_Seal(client, __value);
    }

    std::shared_ptr<Object> _Seal(Client &client, std::shared_ptr<Sequence> &__value) {
        size_t __value_nbytes = 0;

        __value->meta_.SetTypeName(type_name<Sequence>());
        if (std::is_base_of<GlobalObject, Sequence>::value) {
            __value->meta_.SetGlobal(true);
        }

        __value->size_ = size_;
        __value->meta_.AddKeyValue("size_", __value->size_);

        // using __elements__value_type = typename Tuple<std::shared_ptr<Object>>::value_type::element_type;
        using __elements__value_type = typename decltype(__value->elements_)::value_type::element_type;

        size_t __elements__idx = 0;
        for (auto &__elements__value: elements_) {
            auto __value_elements_ = std::dynamic_pointer_cast<__elements__value_type>(
                __elements__value->_Seal(client));
            __value->elements_.emplace_back(__value_elements_);
            __value->meta_.AddMember("__elements_-" + std::to_string(__elements__idx),
                                     __value_elements_);
            __value_nbytes += __value_elements_->nbytes();
            __elements__idx += 1;
        }
        __value->meta_.AddKeyValue("__elements_-size", __value->elements_.size());

        __value->meta_.SetNBytes(__value_nbytes);

        VINEYARD_CHECK_OK(client.CreateMetaData(__value->meta_, __value->id_));

        // mark the builder as sealed
        this->set_sealed(true);

        
        return std::static_pointer_cast<Object>(__value);
    }

    Status Build(Client &client) override {
        return Status::OK();
    }

  protected:
    size_t size_;
    std::vector<std::shared_ptr<ObjectBase>> elements_;

    void set_size_(size_t const &size__) {
        this->size_ = size__;
    }

    void set_elements_(std::vector<std::shared_ptr<ObjectBase>> const &elements__) {
        this->elements_ = elements__;
    }
    void set_elements_(size_t const idx, std::shared_ptr<ObjectBase> const &elements__) {
        if (idx >= this->elements_.size()) {
            this->elements_.resize(idx + 1);
        }
        this->elements_[idx] = elements__;
    }
    void add_elements_(std::shared_ptr<ObjectBase> const &elements__) {
        this->elements_.emplace_back(elements__);
    }

  private:
    friend class Sequence;
};


}  // namespace vineyard



#endif // MODULES_BASIC_DS_SEQUENCE_VINEYARD_H
