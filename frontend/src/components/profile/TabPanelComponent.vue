<template>
  <div class="profile-tab-panel-component">
    <title-component title="Who to follow" />
    <q-list>
      <follow-component
        v-for="(u, i) in randomUsers"
        :key="i"
        :id="u.id"
        :name="u.name"
        :email="u.email"
        :bio="u.bio"
        :profile_image="u.profile_image"
      />
    </q-list>
    <q-btn
      flat
      dense
      :ripple="false"
      label="Show more"
      color="primary"
      size="sm"
    />
    <q-separator />
    <title-component title="Topics to follow" />
    <div class="desc">
      Tweets about the Topics you follow show up in your Home timeline
    </div>
    <div class="chips">
      <q-chip
        v-for="(chip, i) in topics"
        :key="chip.name"
        v-model:selected="chip.value"
        outline
        :ripple="false"
        :disable="chip.disable"
        :removable="!chip.value"
        :color="chip.value ? 'blue-7' : 'secondary'"
        @remove="removeTopic(i)"
      >
        {{ chip.name }}
      </q-chip>
    </div>
    <q-btn
      flat
      dense
      :ripple="false"
      label="More Topics"
      color="primary"
      size="sm"
    />
  </div>
</template>

<script>
import { ref } from "vue";
import { Notify } from "quasar";
import FollowComponent from "../common/RandomFollowListItem.vue";

const users = [
  { name: "대환장 갤러리", nickName: "bighwanjang1" },
  { name: "내가 좋아하는 짤", nickName: "melikezzal", bio: "hello" },
  { name: "힐링짤모으는곳", nickName: "healing_storage", bio: "hello" },
  { name: "대환장 파티", nickName: "bighwanjang_party", bio: "hello" },
  { name: "MBC News (MBC뉴스)", nickName: "mbcnews", bio: "hello" },
  { name: "당근마켓", nickName: "dangen", bio: "hello" },
  { name: "기상천외", nickName: "Kisang", bio: "hello" },
  {
    name: "한국관광공사 :: 대한민국 구석구석",
    nickName: "Kor_Visitkorea",
    bio: "hello",
  },
];

export default {
  name: "TabPanelComponent",
  props: {
    randomUsers: Array,
  },

  setup() {
    const topics = ref([
      { name: "Cats", value: false, disable: false },
      { name: "Dog", value: false, disable: false },
      { name: "Music", value: false, disable: false },
      { name: "Gaming", value: false, disable: false },
      { name: "Marvel Universe", value: false, disable: false },
      { name: "Entertainment", value: false, disable: false },
      { name: "BTS", value: false, disable: false },
      { name: "K-pop", value: false, disable: false },
      { name: "Drink", value: false, disable: false },
      { name: "Pets", value: false, disable: false },
      { name: "Harry Potter", value: false, disable: false },
      { name: "Sugar", value: false, disable: false },
    ]);

    function removeTopic(idx) {
      topics.value[idx].disable = true;
      Notify.create({
        message: "We won’t suggest this Topic anymore.",
        color: "secondary",
        actions: [
          {
            label: "Undo",
            color: "white",
            handler: () => {
              topics.value[idx].disable = false;
            },
          },
        ],
        timeout: 5000,
      });
    }

    return {
      FollowComponent,
      users,

      topics,
      removeTopic,
    };
  },
};
</script>

<style lang="scss">
.profile-tab-panel-component {
  > .q-btn {
    margin: 12px 24px;
  }
  .desc {
    padding: 0 16px;
    margin: -10px 0 12px;
    font-size: 13px;
    color: $grey-7;
  }
  .chips {
    padding: 0 16px;
    .q-chip {
      &__content {
        margin-right: 10px;
      }
    }
  }
}
</style>
