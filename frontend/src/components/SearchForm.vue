<template>
  <q-form
    class="search-form flex row items-center full-width"
    @submit="goSearch"
  >
    <q-input
      v-model="searchInputVal"
      dense
      outlined
      rounded
      clearable
      placeholder="Search"
    >
      <template v-slot:prepend>
        <q-icon name="search" />
      </template>
    </q-input>
  </q-form>
</template>

<script>
import { ref, watch } from "vue";
import { useRouter } from "vue-router";

export default {
  name: 'SearchInput',
  props: {
    searchKeyword: {
      type: String,
      default: '',
    },
  },
  setup(props, { emit }) {
    const router = useRouter();
    const searchInputVal = ref(props.searchKeyword);
    function goSearch() {
      if (searchInputVal.value) {
        router.push(`/search/${searchInputVal.value}`);
        emit('update:keyword', searchInputVal.value)
      }
    }

    watch(() => props.searchKeyword, (newVal, oldVal) => {
      console.log('watch', 'new : ', newVal, 'old : ', oldVal)
    })

    return {
      searchInputVal,
      goSearch,
    }
  },
}
</script>

<style lang="scss">
.search-form {
  .q-field {
    height: 42px;
    min-height: 0;
    width: 100%;
    &.q-field--outlined .q-field__control:after {
      border-width: 1px !important;
    }
    &--focused {
      .q-field__inner {
        .q-field__control {
          .q-field__prepend, .q-field__append {
            .q-icon {
              color: $primary !important;
              opacity: 1;
            }
          }
        }
      }
    }
    &__inner {
      .q-field__control {
        &:before {
          border: none;
          background: $grey-2;
        }
      }
    }
  }
}
</style>
