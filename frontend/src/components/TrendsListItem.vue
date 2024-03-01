<template>
  <q-item clickable class="trends-list-item">
    <q-btn flat dense round unelevated icon="more_horiz" color="grey-7" class="more-btn">
      <q-menu class="trend-list-item-button-menu">
        <q-list>
          <q-item clickable class="flex items-center">
            <q-icon name="sentiment_dissatisfied" />
            <span>Not interested in this</span>
          </q-item>
          <q-item clickable class="flex items-center">
            <q-icon name="sentiment_dissatisfied" />
            <span>This trend is harmful or spammy</span>
          </q-item>
        </q-list>
      </q-menu>
    </q-btn>
    <q-item-section>
      <div class="trend-in">Trending in South Korea</div>
      <div class="keyword">{{ keyword }}</div>
      <div class="tweets">Tweets</div>
    </q-item-section>
  </q-item>
</template>

<script>
export default {
  name: "TrendListItem",
  props: {
    keyword: {
      type: String,
      default: ""
    },
  },
  setup() {
    return {
    }
  },
}
</script>

<style lang="scss">
.trends-list-item {
  padding: 10px 16px;
  position: relative;
  > .more-btn {
    position: absolute;
    top: 6px;
    right: 10px;
    &:hover {
      background: rgba(3, 169, 244, 0.1) !important;
      .q-focus-helper {
        opacity: 0 !important;
        &:before, &:after {
          opacity: 0 !important;
        }
      }
      .q-btn__content {
        .q-icon {
          color: $primary;
        }
      }
    }
    .q-btn__content {
      .q-icon {
        font-size: 18px;
      }
    }
  }
  .q-item__section {
    .trend-in {
      color: $grey-8;
      font-size: 14px;
    }
    .keyword {
      font-weight: 700;
    }
    .tweets {
      color: $grey-8;
      font-size: 13px;
    }
  }
}
.trend-list-item-button-menu {
  max-width: 280px !important;
  width: 280px;
  .q-list {
    padding: 12px 0;
    .q-item {
      min-height: 0;
      padding: 8px 12px;
      font-weight: bold;
      .q-icon {
        font-size: 20px;
        margin-right: 4px;
      }
    }
  }
}
</style>
