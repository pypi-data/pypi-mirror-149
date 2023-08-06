#ifndef MODULES_BASIC_DS_SCALAR_VINEYARD_H
#define MODULES_BASIC_DS_SCALAR_VINEYARD_H

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

#ifndef MODULES_BASIC_DS_SCALAR_MOD_H_
#define MODULES_BASIC_DS_SCALAR_MOD_H_

#include <memory>
#include <string>
#include <utility>
#include <vector>

#include "boost/lexical_cast.hpp"

#include "basic/ds/types.h"
#include "client/client.h"
#include "client/ds/blob.h"
#include "client/ds/i_object.h"
#include "common/util/uuid.h"

namespace vineyard {

#ifdef __GNUC__
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wattributes"
#endif

// NB: the scalar value is write to meta json as a `string` directly,
// without touching shared memory and create a blob.

template <typename T>
class ScalarBaseBuilder;

/**
 * @brief The scalar type in vineyard.
 * Note that the value of the scalar is writing into the
 * meta tree as a `string` directly, instead of storing
 * the value in the shared memory with a blob.
 *
 * @tparam T The type for the value.
 */
template <typename T>
class __attribute__((annotate("vineyard"))) Scalar : public Registered<Scalar<T>> {
 
  public:
    static std::unique_ptr<Object> Create() __attribute__((used)) {
        return std::static_pointer_cast<Object>(
            std::unique_ptr<Scalar<T>>{
                new Scalar<T>()});
    }


  public:
    void Construct(const ObjectMeta& meta) override {
        std::string __type_name = type_name<Scalar<T>>();
        VINEYARD_ASSERT(
            meta.GetTypeName() == __type_name,
            "Expect typename '" + __type_name + "', but got '" + meta.GetTypeName() + "'");
        this->meta_ = meta;
        this->id_ = meta.GetId();

        meta.GetKeyValue("value_", this->value_);
        meta.GetKeyValue("type_", this->type_);

        
    }

 private:
public:
  /**
   * @brief Get the value of the scalar.
   *
   * @return The value of the scalar.
   */
  T const Value() const { return value_; }

  /**
   * @brief Get the type of the scalar.
   *
   * @return The type of the scalar.
   */
  AnyType Type() const { return type_; }

 private:
  __attribute__((annotate("shared"))) T value_;
  __attribute__((annotate("shared"))) AnyType type_ = AnyTypeEnum<T>::value;

  friend class Client;
  friend class ScalarBaseBuilder<T>;
};

#ifdef __GNUC__
#pragma GCC diagnostic pop
#endif

}  // namespace vineyard

#endif  // MODULES_BASIC_DS_SCALAR_MOD_H_

namespace vineyard {

template<typename T>
class ScalarBaseBuilder: public ObjectBuilder {
  public:
    

    explicit ScalarBaseBuilder(Client &client) {}

    explicit ScalarBaseBuilder(
            Scalar<T> const &__value) {
        this->set_value_(__value.value_);
        this->set_type_(__value.type_);
    }

    explicit ScalarBaseBuilder(
            std::shared_ptr<Scalar<T>> const & __value):
        ScalarBaseBuilder(*__value) {
    }

    ObjectMeta &ValueMetaRef(std::shared_ptr<Scalar<T>> &__value) {
        return __value->meta_;
    }

    std::shared_ptr<Object> _Seal(Client &client) override {
        // ensure the builder hasn't been sealed yet.
        ENSURE_NOT_SEALED(this);

        VINEYARD_CHECK_OK(this->Build(client));
        auto __value = std::make_shared<Scalar<T>>();

        return this->_Seal(client, __value);
    }

    std::shared_ptr<Object> _Seal(Client &client, std::shared_ptr<Scalar<T>> &__value) {
        size_t __value_nbytes = 0;

        __value->meta_.SetTypeName(type_name<Scalar<T>>());
        if (std::is_base_of<GlobalObject, Scalar<T>>::value) {
            __value->meta_.SetGlobal(true);
        }

        __value->value_ = value_;
        __value->meta_.AddKeyValue("value_", __value->value_);

        __value->type_ = type_;
        __value->meta_.AddKeyValue("type_", __value->type_);

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
    T value_;
    vineyard::AnyType type_;

    void set_value_(T const &value__) {
        this->value_ = value__;
    }

    void set_type_(vineyard::AnyType const &type__) {
        this->type_ = type__;
    }

  private:
    friend class Scalar<T>;
};


}  // namespace vineyard



#endif // MODULES_BASIC_DS_SCALAR_VINEYARD_H
