#ifndef MODULES_BASIC_DS_ARRAY_VINEYARD_H
#define MODULES_BASIC_DS_ARRAY_VINEYARD_H

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

#ifndef MODULES_BASIC_DS_ARRAY_MOD_H_
#define MODULES_BASIC_DS_ARRAY_MOD_H_

#include <cstdint>
#include <memory>
#include <string>
#include <utility>
#include <vector>

#include "client/client.h"
#include "client/ds/blob.h"
#include "client/ds/i_object.h"
#include "common/util/uuid.h"

namespace vineyard {

template <typename T>
class ArrayBaseBuilder;

#ifdef __GNUC__
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wattributes"
#endif

/**
 * @brief The array type in vineyard.
 *
 * @tparam T The type for the elements.
 */
template <typename T>
class __attribute__((annotate("vineyard"))) Array : public Registered<Array<T>> {
 
  public:
    static std::unique_ptr<Object> Create() __attribute__((used)) {
        return std::static_pointer_cast<Object>(
            std::unique_ptr<Array<T>>{
                new Array<T>()});
    }


  public:
    void Construct(const ObjectMeta& meta) override {
        std::string __type_name = type_name<Array<T>>();
        VINEYARD_ASSERT(
            meta.GetTypeName() == __type_name,
            "Expect typename '" + __type_name + "', but got '" + meta.GetTypeName() + "'");
        this->meta_ = meta;
        this->id_ = meta.GetId();

        meta.GetKeyValue("size_", this->size_);
        this->buffer_ = std::dynamic_pointer_cast<Blob>(meta.GetMember("buffer_"));

        
    }

 private:
public:
  /**
   * @brief Get the element at the given location.
   *
   * @param loc The given location to get the element.
   */
  __attribute__((annotate("shared"))) const T& operator[](size_t loc) const { return data()[loc]; }

  /**
   * @brief Get the size of the array.
   *
   * @return The size.
   */
  __attribute__((annotate("shared"))) size_t size() const { return size_; }

  /**
   * @brief Get the pointer to the beginning of the data buffer
   *
   * @param The pointer to the data buffer
   */
  __attribute__((annotate("shared"))) const T* data() const {
    return reinterpret_cast<const T*>(buffer_->data());
  }

 private:
  __attribute__((annotate("shared"))) size_t size_;
  __attribute__((annotate("shared"))) std::shared_ptr<Blob> buffer_;

  friend class Client;
  friend class ArrayBaseBuilder<T>;
};

#ifdef __GNUC__
#pragma GCC diagnostic pop
#endif
}  // namespace vineyard

#endif  // MODULES_BASIC_DS_ARRAY_MOD_H_

namespace vineyard {

template<typename T>
class ArrayBaseBuilder: public ObjectBuilder {
  public:
    

    explicit ArrayBaseBuilder(Client &client) {}

    explicit ArrayBaseBuilder(
            Array<T> const &__value) {
        this->set_size_(__value.size_);
        this->set_buffer_(__value.buffer_);
    }

    explicit ArrayBaseBuilder(
            std::shared_ptr<Array<T>> const & __value):
        ArrayBaseBuilder(*__value) {
    }

    ObjectMeta &ValueMetaRef(std::shared_ptr<Array<T>> &__value) {
        return __value->meta_;
    }

    std::shared_ptr<Object> _Seal(Client &client) override {
        // ensure the builder hasn't been sealed yet.
        ENSURE_NOT_SEALED(this);

        VINEYARD_CHECK_OK(this->Build(client));
        auto __value = std::make_shared<Array<T>>();

        return this->_Seal(client, __value);
    }

    std::shared_ptr<Object> _Seal(Client &client, std::shared_ptr<Array<T>> &__value) {
        size_t __value_nbytes = 0;

        __value->meta_.SetTypeName(type_name<Array<T>>());
        if (std::is_base_of<GlobalObject, Array<T>>::value) {
            __value->meta_.SetGlobal(true);
        }

        __value->size_ = size_;
        __value->meta_.AddKeyValue("size_", __value->size_);

        // using __buffer__value_type = typename std::shared_ptr<Blob>::element_type;
        using __buffer__value_type = typename decltype(__value->buffer_)::element_type;
        auto __value_buffer_ = std::dynamic_pointer_cast<__buffer__value_type>(
            buffer_->_Seal(client));
        __value->buffer_ = __value_buffer_;
        __value->meta_.AddMember("buffer_", __value->buffer_);
        __value_nbytes += __value_buffer_->nbytes();

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
    std::shared_ptr<ObjectBase> buffer_;

    void set_size_(size_t const &size__) {
        this->size_ = size__;
    }

    void set_buffer_(std::shared_ptr<ObjectBase> const & buffer__) {
        this->buffer_ = buffer__;
    }

  private:
    friend class Array<T>;
};


}  // namespace vineyard



#endif // MODULES_BASIC_DS_ARRAY_VINEYARD_H
