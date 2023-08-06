#ifndef MODULES_BASIC_DS_HASHMAP_VINEYARD_H
#define MODULES_BASIC_DS_HASHMAP_VINEYARD_H

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

#ifndef MODULES_BASIC_DS_HASHMAP_MOD_H_
#define MODULES_BASIC_DS_HASHMAP_MOD_H_

#include <algorithm>
#include <functional>
#include <memory>
#include <string>
#include <utility>

#include "flat_hash_map/flat_hash_map.hpp"

#include "basic/ds/array.vineyard.h"
#include "client/ds/blob.h"
#include "client/ds/i_object.h"
#include "common/util/uuid.h"

namespace vineyard {

#ifdef __GNUC__
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wattributes"
#endif

struct prime_hash_policy {
  prime_hash_policy() : current_prime_(1) {}
  prime_hash_policy(const prime_hash_policy& rhs)
      : current_prime_(rhs.current_prime_) {}
  prime_hash_policy& operator=(const prime_hash_policy& rhs) {
    current_prime_ = rhs.current_prime_;
    return *this;
  }

  size_t index_for_hash(size_t hash) const { return hash % current_prime_; }

  void set_prime(size_t prime) { current_prime_ = prime; }

 private:
  size_t current_prime_;
};

template <typename K, typename V, typename H, typename E>
class HashmapBaseBuilder;

/**
 * @brief The hash map in vineyard.
 *
 * @tparam K The type for the key.
 * @tparam V The type for the value.
 * @tparam std::hash<K> The hash function for the key.
 * @tparam std::equal_to<K> The compare function for the key.
 */
template <typename K, typename V, typename H = std::hash<K>,
          typename E = std::equal_to<K>>
class __attribute__((annotate("vineyard"))) Hashmap : public Registered<Hashmap<K, V, H, E>>,
                             public H,
                             public E {
 
  public:
    static std::unique_ptr<Object> Create() __attribute__((used)) {
        return std::static_pointer_cast<Object>(
            std::unique_ptr<Hashmap<K, V, H, E>>{
                new Hashmap<K, V, H, E>()});
    }


  public:
    void Construct(const ObjectMeta& meta) override {
        std::string __type_name = type_name<Hashmap<K, V, H, E>>();
        VINEYARD_ASSERT(
            meta.GetTypeName() == __type_name,
            "Expect typename '" + __type_name + "', but got '" + meta.GetTypeName() + "'");
        this->meta_ = meta;
        this->id_ = meta.GetId();

        meta.GetKeyValue("num_slots_minus_one_", this->num_slots_minus_one_);
        meta.GetKeyValue("max_lookups_", this->max_lookups_);
        meta.GetKeyValue("num_elements_", this->num_elements_);
        this->entries_.Construct(meta.GetMemberMeta("entries_"));

        
        if (meta.IsLocal()) {
            this->PostConstruct(meta);
        }
    }

 private:
public:
  using T = std::pair<K, V>;

  using Entry = ska::detailv3::sherwood_v3_entry<T>;
  using EntryPointer = const Entry*;

  using Hasher = ska::detailv3::KeyOrValueHasher<K, std::pair<K, V>, H>;
  using Equal = ska::detailv3::KeyOrValueEquality<K, std::pair<K, V>, E>;

  /**
   * @brief Set the hash policy after the construction of the HashMap.
   *
   */
  void PostConstruct(const ObjectMeta& meta) override {
    hash_policy_.set_prime(num_slots_minus_one_ + 1);
  }

  using value_type = T;
  using size_type = size_t;
  using difference_type = std::ptrdiff_t;
  using hasher = H;
  using key_equal = E;
  using reference = value_type&;
  using const_reference = const value_type&;
  using pointer = value_type*;
  using const_pointer = value_type*;

  using flat_hash_table_type = ska::detailv3::sherwood_v3_table<
      T, K, H, Hasher, E, Equal, std::allocator<T>,
      typename std::allocator_traits<std::allocator<T>>::template rebind_alloc<
          ska::detailv3::sherwood_v3_entry<T>>>;

  /**
   * @brief The iterator to iterate key-value mappings in the HashMap.
   *
   */
  struct iterator {
    iterator() = default;
    explicit iterator(EntryPointer current) : current(current) {}
    EntryPointer current = EntryPointer();

    friend bool operator==(const iterator& lhs, const iterator& rhs) {
      return lhs.current == rhs.current;
    }

    friend bool operator!=(const iterator& lhs, const iterator& rhs) {
      return lhs.current != rhs.current;
    }

    iterator& operator++() {
      do {
        ++current;
      } while (current->is_empty());
      return *this;
    }

    iterator operator++(int) {
      iterator copy(*this);
      ++*this;
      return copy;
    }

    const value_type& operator*() const { return current->value; }

    const value_type* operator->() const {
      return std::addressof(current->value);
    }
  };

  /**
   * @brief The beginning iterator.
   *
   */
  iterator begin() const {
    for (EntryPointer it = entries_.data();; ++it) {
      if (it->has_value()) {
        return iterator(it);
      }
    }
  }

  /**
   * @brief The ending iterator.
   *
   */
  iterator end() const {
    return iterator(entries_.data() + static_cast<ptrdiff_t>(
                                          num_slots_minus_one_ + max_lookups_));
  }

  /**
   * @brief Find the iterator by key.
   *
   */
  iterator find(const K& key) {
    size_t index = hash_policy_.index_for_hash(hash_object(key));
    EntryPointer it = entries_.data() + static_cast<ptrdiff_t>(index);
    for (int8_t distance = 0; it->distance_from_desired >= distance;
         ++distance, ++it) {
      if (compares_equal(key, it->value.first)) {
        return iterator(it);
      }
    }
    return end();
  }

  /**
   * @brief Return the const iterator by key.
   *
   */
  const iterator find(const K& key) const {
    return const_cast<Hashmap<K, V, H, E>*>(this)->find(key);
  }

  /**
   * @brief Return the number of occurancies of the key.
   *
   */
  size_t count(const K& key) const { return find(key) == end() ? 0 : 1; }

  /**
   * @brief Return the size of the HashMap, i.e., the number of elements stored
   * in the HashMap.
   *
   */
  size_t size() const { return num_elements_; }

  /**
   * @brief Check whether the HashMap is empty.
   *
   */
  bool empty() const { return num_elements_ == 0; }

  /**
   * @brief Get the value by key.
   * Here the existance of the key is checked.
   */
  const V& at(const K& key) const {
    auto found = this->find(key);
    if (found == this->end()) {
      throw std::out_of_range("Argument passed to at() was not in the map.");
    }
    return found->second;
  }

 private:
  __attribute__((annotate("shared"))) size_t num_slots_minus_one_;
  __attribute__((annotate("shared"))) int8_t max_lookups_;
  __attribute__((annotate("shared"))) size_t num_elements_;
  __attribute__((annotate("shared"))) Array<Entry> entries_;

  prime_hash_policy hash_policy_;

  friend class Client;
  friend class HashmapBaseBuilder<K, V, H, E>;

  size_t hash_object(const K& key) const {
    return static_cast<const H&>(*this)(key);
  }

  bool compares_equal(const K& lhs, const K& rhs) const {
    return static_cast<const E&>(*this)(lhs, rhs);
  }
};

#ifdef __GNUC__
#pragma GCC diagnostic pop
#endif

}  // namespace vineyard

#endif  // MODULES_BASIC_DS_HASHMAP_MOD_H_

namespace vineyard {

template<typename K, typename V, typename H = std::hash<K>, typename E = std::equal_to<K>>
class HashmapBaseBuilder: public ObjectBuilder {
  public:
    // using T
    using T = std::pair<K, V>;
    // using Entry
    using Entry = ska::detailv3::sherwood_v3_entry<T>;
    // using EntryPointer
    using EntryPointer = const Entry*;
    // using Hasher
    using Hasher = ska::detailv3::KeyOrValueHasher<K, std::pair<K, V>, H>;
    // using Equal
    using Equal = ska::detailv3::KeyOrValueEquality<K, std::pair<K, V>, E>;
    // using value_type
    using value_type = T;
    // using size_type
    using size_type = size_t;
    // using difference_type
    using difference_type = std::ptrdiff_t;
    // using hasher
    using hasher = H;
    // using key_equal
    using key_equal = E;
    // using reference
    using reference = value_type&;
    // using const_reference
    using const_reference = const value_type&;
    // using pointer
    using pointer = value_type*;
    // using const_pointer
    using const_pointer = value_type*;
    // using flat_hash_table_type
    using flat_hash_table_type = ska::detailv3::sherwood_v3_table<
      T, K, H, Hasher, E, Equal, std::allocator<T>,
      typename std::allocator_traits<std::allocator<T>>::template rebind_alloc<
          ska::detailv3::sherwood_v3_entry<T>>>;

    explicit HashmapBaseBuilder(Client &client) {}

    explicit HashmapBaseBuilder(
            Hashmap<K, V, H, E> const &__value) {
        this->set_num_slots_minus_one_(__value.num_slots_minus_one_);
        this->set_max_lookups_(__value.max_lookups_);
        this->set_num_elements_(__value.num_elements_);
        this->set_entries_(
            std::make_shared<typename std::decay<decltype(__value.entries_)>::type>(
                __value.entries_));
    }

    explicit HashmapBaseBuilder(
            std::shared_ptr<Hashmap<K, V, H, E>> const & __value):
        HashmapBaseBuilder(*__value) {
    }

    ObjectMeta &ValueMetaRef(std::shared_ptr<Hashmap<K, V, H, E>> &__value) {
        return __value->meta_;
    }

    std::shared_ptr<Object> _Seal(Client &client) override {
        // ensure the builder hasn't been sealed yet.
        ENSURE_NOT_SEALED(this);

        VINEYARD_CHECK_OK(this->Build(client));
        auto __value = std::make_shared<Hashmap<K, V, H, E>>();

        return this->_Seal(client, __value);
    }

    std::shared_ptr<Object> _Seal(Client &client, std::shared_ptr<Hashmap<K, V, H, E>> &__value) {
        size_t __value_nbytes = 0;

        __value->meta_.SetTypeName(type_name<Hashmap<K, V, H, E>>());
        if (std::is_base_of<GlobalObject, Hashmap<K, V, H, E>>::value) {
            __value->meta_.SetGlobal(true);
        }

        __value->num_slots_minus_one_ = num_slots_minus_one_;
        __value->meta_.AddKeyValue("num_slots_minus_one_", __value->num_slots_minus_one_);

        __value->max_lookups_ = max_lookups_;
        __value->meta_.AddKeyValue("max_lookups_", __value->max_lookups_);

        __value->num_elements_ = num_elements_;
        __value->meta_.AddKeyValue("num_elements_", __value->num_elements_);

        // using __entries__value_type = typename Array<vineyard::Hashmap::Entry>;
        using __entries__value_type = decltype(__value->entries_);
        auto __value_entries_ = std::dynamic_pointer_cast<__entries__value_type>(
            entries_->_Seal(client));
        __value->entries_ = *__value_entries_;
        __value->meta_.AddMember("entries_", __value->entries_);
        __value_nbytes += __value_entries_->nbytes();

        __value->meta_.SetNBytes(__value_nbytes);

        VINEYARD_CHECK_OK(client.CreateMetaData(__value->meta_, __value->id_));

        // mark the builder as sealed
        this->set_sealed(true);

        
        // run `PostConstruct` to return a valid object
        __value->PostConstruct(__value->meta_);

        return std::static_pointer_cast<Object>(__value);
    }

    Status Build(Client &client) override {
        return Status::OK();
    }

  protected:
    size_t num_slots_minus_one_;
    int8_t max_lookups_;
    size_t num_elements_;
    std::shared_ptr<ObjectBase> entries_;

    void set_num_slots_minus_one_(size_t const &num_slots_minus_one__) {
        this->num_slots_minus_one_ = num_slots_minus_one__;
    }

    void set_max_lookups_(int8_t const &max_lookups__) {
        this->max_lookups_ = max_lookups__;
    }

    void set_num_elements_(size_t const &num_elements__) {
        this->num_elements_ = num_elements__;
    }

    void set_entries_(std::shared_ptr<ObjectBase> const & entries__) {
        this->entries_ = entries__;
    }

  private:
    friend class Hashmap<K, V, H, E>;
};


}  // namespace vineyard



#endif // MODULES_BASIC_DS_HASHMAP_VINEYARD_H
