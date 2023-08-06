#ifndef MODULES_BASIC_DS_DATAFRAME_VINEYARD_H
#define MODULES_BASIC_DS_DATAFRAME_VINEYARD_H

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

#ifndef MODULES_BASIC_DS_DATAFRAME_MOD_H_
#define MODULES_BASIC_DS_DATAFRAME_MOD_H_

#include <algorithm>
#include <functional>
#include <map>
#include <memory>
#include <set>
#include <string>
#include <tuple>
#include <unordered_map>
#include <utility>
#include <vector>

#include "arrow/api.h"
#include "arrow/io/api.h"

#include "basic/ds/array.vineyard.h"
#include "basic/ds/arrow.vineyard.h"
#include "basic/ds/tensor.vineyard.h"
#include "client/client.h"
#include "client/ds/i_object.h"
#include "client/ds/stream.h"
#include "common/util/json.h"

namespace vineyard {

#ifdef __GNUC__
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wattributes"
#endif

class DataFrameBaseBuilder;

class __attribute__((annotate("vineyard(streamable)"))) DataFrame : public Registered<DataFrame> {
 
  public:
    static std::unique_ptr<Object> Create() __attribute__((used)) {
        return std::static_pointer_cast<Object>(
            std::unique_ptr<DataFrame>{
                new DataFrame()});
    }


  public:
    void Construct(const ObjectMeta& meta) override {
        std::string __type_name = type_name<DataFrame>();
        VINEYARD_ASSERT(
            meta.GetTypeName() == __type_name,
            "Expect typename '" + __type_name + "', but got '" + meta.GetTypeName() + "'");
        this->meta_ = meta;
        this->id_ = meta.GetId();

        meta.GetKeyValue("partition_index_row_", this->partition_index_row_);
        meta.GetKeyValue("partition_index_column_", this->partition_index_column_);
        meta.GetKeyValue("row_batch_index_", this->row_batch_index_);
        meta.GetKeyValue("columns_", this->columns_);
        for (size_t __idx = 0; __idx < meta.GetKeyValue<size_t>("__values_-size"); ++__idx) {
            this->values_.emplace(meta.GetKeyValue<vineyard::json>("__values_-key-" + std::to_string(__idx)),
                    std::dynamic_pointer_cast<ITensor>(
                            meta.GetMember("__values_-value-" + std::to_string(__idx))));
        }

        
    }

 private:
public:
  /**
   * @brief Get the column names.
   *
   * @return The vector of column names.
   */
  const std::vector<json>& Columns() const;

  /**
   * @brief Get the index of dataframe.
   *
   * @return The shared pointer to the index tensor.
   */
  std::shared_ptr<ITensor> Index() const;

  /**
   * @brief Get the column of the given column name.
   *
   * @param column The given column name.
   * @return The shared pointer to the column tensor.
   */
  std::shared_ptr<ITensor> Column(json const& column) const;

  /**
   * @brief Get the partition index of the global dataframe.
   *
   * @return The pair of the partition_index on rows and the partition_index on
   * columns.
   */
  const std::pair<size_t, size_t> partition_index() const;

  /**
   * @brief Get the shape of the dataframe.
   *
   * @return The pair of the number of rows and the number of columns.
   */
  const std::pair<size_t, size_t> shape() const;

  /**
   * @brief Get a RecordBatch view for the dataframe.
   */
  const std::shared_ptr<arrow::RecordBatch> AsBatch(bool copy = false) const;

 private:
  __attribute__((annotate("shared"))) size_t partition_index_row_;
  __attribute__((annotate("shared"))) size_t partition_index_column_;

  __attribute__((annotate("shared"))) size_t row_batch_index_;

  __attribute__((annotate("shared"))) Tuple<json> columns_;
  __attribute__((annotate("shared"))) Map<json, std::shared_ptr<ITensor>> values_;

  friend class Client;
  friend class DataFrameBaseBuilder;
};

#ifdef __GNUC__
#pragma GCC diagnostic pop
#endif

}  // namespace vineyard

#endif  // MODULES_BASIC_DS_DATAFRAME_MOD_H_

namespace vineyard {


class DataFrameBaseBuilder: public ObjectBuilder {
  public:
    

    explicit DataFrameBaseBuilder(Client &client) {}

    explicit DataFrameBaseBuilder(
            DataFrame const &__value) {
        this->set_partition_index_row_(__value.partition_index_row_);
        this->set_partition_index_column_(__value.partition_index_column_);
        this->set_row_batch_index_(__value.row_batch_index_);
        this->set_columns_(__value.columns_);
        for (auto const &__values__item_kv: __value.values_) {
            this->set_values_(__values__item_kv.first,
                                   __values__item_kv.second);
        }
    }

    explicit DataFrameBaseBuilder(
            std::shared_ptr<DataFrame> const & __value):
        DataFrameBaseBuilder(*__value) {
    }

    ObjectMeta &ValueMetaRef(std::shared_ptr<DataFrame> &__value) {
        return __value->meta_;
    }

    std::shared_ptr<Object> _Seal(Client &client) override {
        // ensure the builder hasn't been sealed yet.
        ENSURE_NOT_SEALED(this);

        VINEYARD_CHECK_OK(this->Build(client));
        auto __value = std::make_shared<DataFrame>();

        return this->_Seal(client, __value);
    }

    std::shared_ptr<Object> _Seal(Client &client, std::shared_ptr<DataFrame> &__value) {
        size_t __value_nbytes = 0;

        __value->meta_.SetTypeName(type_name<DataFrame>());
        if (std::is_base_of<GlobalObject, DataFrame>::value) {
            __value->meta_.SetGlobal(true);
        }

        __value->partition_index_row_ = partition_index_row_;
        __value->meta_.AddKeyValue("partition_index_row_", __value->partition_index_row_);

        __value->partition_index_column_ = partition_index_column_;
        __value->meta_.AddKeyValue("partition_index_column_", __value->partition_index_column_);

        __value->row_batch_index_ = row_batch_index_;
        __value->meta_.AddKeyValue("row_batch_index_", __value->row_batch_index_);

        __value->columns_ = columns_;
        __value->meta_.AddKeyValue("columns_", __value->columns_);

        // using __values__value_type = typename Map<vineyard::json, std::shared_ptr<ITensor>>::mapped_type::element_type;
        using __values__value_type = typename decltype(__value->values_)::mapped_type::element_type;

        size_t __values__idx = 0;
        for (auto &__values__kv: values_) {
            auto __value_values_ = std::dynamic_pointer_cast<__values__value_type>(
                __values__kv.second->_Seal(client));
            __value->values_.emplace(__values__kv.first, __value_values_);
            __value->meta_.AddKeyValue("__values_-key-" + std::to_string(__values__idx),
                                        __values__kv.first);
            __value->meta_.AddMember("__values_-value-" + std::to_string(__values__idx),
                                     __value_values_);
            __value_nbytes += __value_values_->nbytes();
            __values__idx += 1;
        }
        __value->meta_.AddKeyValue("__values_-size", __value->values_.size());

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
    size_t partition_index_row_;
    size_t partition_index_column_;
    size_t row_batch_index_;
    Tuple<vineyard::json> columns_;
    std::map<typename Map<vineyard::json, std::shared_ptr<ITensor>>::key_type, std::shared_ptr<ObjectBase>> values_;

    void set_partition_index_row_(size_t const &partition_index_row__) {
        this->partition_index_row_ = partition_index_row__;
    }

    void set_partition_index_column_(size_t const &partition_index_column__) {
        this->partition_index_column_ = partition_index_column__;
    }

    void set_row_batch_index_(size_t const &row_batch_index__) {
        this->row_batch_index_ = row_batch_index__;
    }

    void set_columns_(Tuple<vineyard::json> const &columns__) {
        this->columns_ = columns__;
    }

    void set_values_(std::map<typename Map<vineyard::json, std::shared_ptr<ITensor>>::key_type, std::shared_ptr<ObjectBase>> const &values__) {
        this->values_ = values__;
    }
    // FIXME: set a corresponding builder, rather than ObjectBase.
    void set_values_(typename Map<vineyard::json, std::shared_ptr<ITensor>>::key_type const &values__key_,
                           std::shared_ptr<ObjectBase> values__value_) {
        this->values_.emplace(values__key_, values__value_);
    }

  private:
    friend class DataFrame;
};


}  // namespace vineyard




namespace vineyard {


using DataFrameStreamBase = vineyard::Stream<DataFrame>;


}  // namespace vineyard



#endif // MODULES_BASIC_DS_DATAFRAME_VINEYARD_H
