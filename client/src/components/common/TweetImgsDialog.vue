<template>
  <q-dialog ref="dialogRef" class="tweet-imgs-dialog">
    <q-card>
      <q-card-action class="top-action-container absolute flex items-center justify-between q-pa-md">
        <q-btn round icon="close" color="black" @click="onDialogCancel" />
        <q-btn round icon="more_horiz" color="black" />
      </q-card-action>
      <q-card-section class="flex items-center justify-center">
        <q-carousel
          swipeable
          animated
          infinite
          v-model="slide"
          arrows
          control-type="regular"
          control-color="black"
          control-text-color="white"
        >
          <q-carousel-slide
            v-for="(upload, i) in uploads"
            :key="i"
            :name="i"
            :img-src="`/uploads/${upload}`"
          />
        </q-carousel>
      </q-card-section>

      <q-card-action class="function-container flex items-center justify-around">
        <q-btn flat rounded :label="Number(10).toLocaleString()" :icon="roundComment" color="white" />
        <q-btn flat rounded :label="Number(1200).toLocaleString()" :icon="roundCached" color="white" />
        <q-btn
          flat
          rounded
          :label="Number(like_count).toLocaleString()"
          :icon="like ? roundFavorite : roundFavoriteBorder"
          color="white"
          @click="clickLike"
        />
        <q-btn flat round :icon="roundIosShare" color="white" />
      </q-card-action>

    </q-card>
  </q-dialog>
</template>

<script>
import { ref } from 'vue';
import { useDialogPluginComponent, Cookies } from "quasar";
import {
  roundComment,
  roundCached,
  roundFavoriteBorder,
  roundFavorite,
  roundIosShare,
} from "@quasar/extras/material-icons-round";

export default {
  name: "TweetImgsDialog",
  props: {
    uploads: Array,
    idx: Number,
    id: Number,
    like: Boolean,
    like_count: Number
  },
  setup(props) {
    const { dialogRef, onDialogCancel } =
      useDialogPluginComponent();

    const slide = ref(props.idx);

    const myId = ref(Cookies.get("user").id)
    function clickLike() {
    }

    return {
      dialogRef,
      onDialogCancel,

      roundComment,
      roundCached,
      roundFavoriteBorder,
      roundFavorite,
      roundIosShare,

      slide,
      clickLike
    };
  },
};
</script>

<style lang="scss">
.tweet-imgs-dialog {
  .q-dialog__backdrop {
    background: rgba(0,0,0,.9);
  }
  .q-dialog__inner {
    padding: 0;
    display: block;
    .q-card {
      width: 100%;
      height: 100%;
      max-width: 100%;
      max-height: 100%;
      background: none;
      position: relative;
      border-radius: 0;

      .top-action-container {
        width: 100%;
        z-index: 1;
      }

      .q-card__section {
        height: calc(100% - 58px);
        width: 100%;
        .q-carousel {
          width: 100%;
          height: 100%;
          background: none;
          .q-carousel__slides-container {
            .q-panel {
              .q-carousel__slide {
                background-repeat: no-repeat;
                background-size: contain;


              }

            }

          }
        }
      }


      .function-container {
        padding: 8px 0;

      }
    }
  }
}
</style>
