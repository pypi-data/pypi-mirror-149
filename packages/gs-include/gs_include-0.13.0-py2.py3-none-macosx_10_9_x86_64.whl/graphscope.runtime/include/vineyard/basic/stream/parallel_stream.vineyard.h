#ifndef MODULES_BASIC_STREAM_PARALLEL_STREAM_VINEYARD_H
#define MODULES_BASIC_STREAM_PARALLEL_STREAM_VINEYARD_H

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

#ifndef MODULES_BASIC_STREAM_PARALLEL_STREAM_MOD_H_
#define MODULES_BASIC_STREAM_PARALLEL_STREAM_MOD_H_

#include <memory>
#include <string>
#include <vector>

#include "client/client.h"
#include "client/ds/core_types.h"
#include "client/ds/i_object.h"

namespace vineyard {

class ParallelStreamBaseBuilder;

class __attribute__((annotate("vineyard"))) ParallelStream : public Registered<ParallelStream>,
                                    GlobalObject {
 
  public:
    static std::unique_ptr<Object> Create() __attribute__((used)) {
        return std::static_pointer_cast<Object>(
            std::unique_ptr<ParallelStream>{
                new ParallelStream()});
    }


  public:
    void Construct(const ObjectMeta& meta) override {
        std::string __type_name = type_name<ParallelStream>();
        VINEYARD_ASSERT(
            meta.GetTypeName() == __type_name,
            "Expect typename '" + __type_name + "', but got '" + meta.GetTypeName() + "'");
        this->meta_ = meta;
        this->id_ = meta.GetId();

        for (size_t __idx = 0; __idx < meta.GetKeyValue<size_t>("__streams_-size"); ++__idx) {
            this->streams_.emplace_back(std::dynamic_pointer_cast<Object>(
                    meta.GetMember("__streams_-" + std::to_string(__idx))));
        }

        
    }


    size_t size() const {
        return this->streams_.size();
    }

    Tuple<std::shared_ptr<Object>>::value_type Get(const size_t index) const {
        return this->streams_[index];
    }

    ObjectMeta GetMeta(const size_t index) const {
        return this->streams_[index]->meta();
    }

    Tuple<Tuple<std::shared_ptr<Object>>::value_type> const &GetAll() const {
        return this->streams_;
    }

    template <typename T>
    size_t GetLocals(Tuple<std::shared_ptr<T>> &locals) const {
        size_t __local_size = 0;
        for (auto const &__e: this->streams_) {
            if (__e->IsLocal()) {
                locals.emplace_back(std::dynamic_pointer_cast<T>(__e));
            }
        }
        return __local_size;
    }

    Tuple<Tuple<std::shared_ptr<Object>>::value_type> GetLocals() const {
        Tuple<Tuple<std::shared_ptr<Object>>::value_type> __locals;
        for (auto const &__e: this->streams_) {
            if (__e->IsLocal()) {
                __locals.emplace_back(__e);
            }
        }
        return __locals;
    }

 private:
private:
  __attribute__((annotate("distributed"))) Tuple<std::shared_ptr<Object>> streams_;

  friend class ParallelStreamBaseBuilder;
};

}  // namespace vineyard

#endif  // MODULES_BASIC_STREAM_PARALLEL_STREAM_MOD_H_

namespace vineyard {


class ParallelStreamBaseBuilder: public ObjectBuilder {
  public:
    

    explicit ParallelStreamBaseBuilder(Client &client) {}

    explicit ParallelStreamBaseBuilder(
            ParallelStream const &__value) {
        for (auto const &__streams__item: __value.streams_) {
            this->add_streams_(__streams__item);
        }
    }

    explicit ParallelStreamBaseBuilder(
            std::shared_ptr<ParallelStream> const & __value):
        ParallelStreamBaseBuilder(*__value) {
    }

    ObjectMeta &ValueMetaRef(std::shared_ptr<ParallelStream> &__value) {
        return __value->meta_;
    }

    std::shared_ptr<Object> _Seal(Client &client) override {
        // ensure the builder hasn't been sealed yet.
        ENSURE_NOT_SEALED(this);

        VINEYARD_CHECK_OK(this->Build(client));
        auto __value = std::make_shared<ParallelStream>();

        return this->_Seal(client, __value);
    }

    std::shared_ptr<Object> _Seal(Client &client, std::shared_ptr<ParallelStream> &__value) {
        size_t __value_nbytes = 0;

        __value->meta_.SetTypeName(type_name<ParallelStream>());
        if (std::is_base_of<GlobalObject, ParallelStream>::value) {
            __value->meta_.SetGlobal(true);
        }

        // using __streams__value_type = typename Tuple<std::shared_ptr<Object>>::value_type::element_type;
        using __streams__value_type = typename decltype(__value->streams_)::value_type::element_type;

        size_t __streams__idx = 0;
        for (auto &__streams__value: streams_) {
            auto __value_streams_ = std::dynamic_pointer_cast<__streams__value_type>(
                __streams__value->_Seal(client));
            __value->streams_.emplace_back(__value_streams_);
            __value->meta_.AddMember("__streams_-" + std::to_string(__streams__idx),
                                     __value_streams_);
            __value_nbytes += __value_streams_->nbytes();
            __streams__idx += 1;
        }
        __value->meta_.AddKeyValue("__streams_-size", __value->streams_.size());

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
    std::vector<std::shared_ptr<ObjectBase>> streams_;

    void set_streams_(std::vector<std::shared_ptr<ObjectBase>> const &streams__) {
        this->streams_ = streams__;
    }
    void set_streams_(size_t const idx, std::shared_ptr<ObjectBase> const &streams__) {
        if (idx >= this->streams_.size()) {
            this->streams_.resize(idx + 1);
        }
        this->streams_[idx] = streams__;
    }
    void add_streams_(std::shared_ptr<ObjectBase> const &streams__) {
        this->streams_.emplace_back(streams__);
    }

  private:
    friend class ParallelStream;
};


}  // namespace vineyard



#endif // MODULES_BASIC_STREAM_PARALLEL_STREAM_VINEYARD_H
