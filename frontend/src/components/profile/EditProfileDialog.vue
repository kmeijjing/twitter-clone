<template>
  <q-dialog ref="dialogRef" class="edit-profile-dialog">
    <q-card>
      <q-card-section class="dialog-header flex row items-center" flat>
        <q-btn
          flat
          dense
          round
          :ripple="false"
          icon="close"
          class="close-btn"
          @click="onDialogCancel"
        />
        <div class="title">Edit profile</div>
        <q-btn
          rounded
          no-caps
          unelevated
          color="black"
          label="Save"
          class="save-btn"
          @click="saveUserInfo(userInfo)"
        />
      </q-card-section>

      <q-scroll-area style="height: 550px">
        <q-card-section class="profile-card-container" flat>
          <div class="photo-section">
            <div class="bg-image">
              <q-img
                v-if="userInfo.bgImage"
                :src="`bgImgs/${userInfo.user_id}/${userInfo.bgImage}`"
                style="height: 180px"
              />
              <q-img
                v-else
                :src="bgImageSrc"
                style="height: 180px"
              />
              <div class="edit-bg-image">
                <q-icon name="add_a_photo" color="grey-1" />
                <q-file
                  dense
                  borderless
                  v-model="bgImageVal"
                  accept="image/*"
                  :max-file-size="2097152"
                  :max-files="1"
                  class="cursor-pointer"
                  @update:modelValue="updateBgImage"
                />
              </div>
            </div>
            <div class="profile-image">
              <q-avatar>
                <img
                  :src="userInfo.profileImage
                    ? `profileImgs/${userInfo.user_id}/${userInfo.profileImage}`
                    : profileImageSrc"
                />
              </q-avatar>
              <div class="edit-profile-image">
                <q-icon name="add_a_photo" color="grey-1" />
                <q-file
                  dense
                  borderless
                  v-model="profileImageVal"
                  accept="image/*"
                  :max-file-size="2097152"
                  :max-files="1"
                  class="cursor-pointer"
                  @update:modelValue="updateProfileImage"
                />
              </div>
            </div>
          </div>

          <q-form>
            <q-input
              v-model="userInfo.name"
              outlined
              dense
              counter
              maxlength="50"
              label="Name"
              autofocus
            />
            <q-input
              v-model="userInfo.bio"
              outlined
              dense
              counter
              maxlength="160"
              label="Bio"
            />
            <q-input
              v-model="userInfo.location"
              outlined
              dense
              counter
              maxlength="30"
              label="Location"
            />
            <q-input
              v-model="userInfo.website"
              outlined
              dense
              counter
              maxlength="100"
              label="Website"
            />
            <q-input
              v-model="userInfo.birth"
              type="date"
              outlined
              dense
              counter
              maxlength="100"
              label="Birth"
            />
          </q-form>
        </q-card-section>
      </q-scroll-area>
    </q-card>
  </q-dialog>
</template>

<script>
import { ref } from "vue";
import { useDialogPluginComponent } from "quasar";
import { api } from "@boot/axios"

export default {
  components: {},
  props: {
    user: Object,
  },
  setup(props) {
    const { dialogRef, onDialogOK, onDialogCancel } =
      useDialogPluginComponent();

    const userInfo = ref({
      user_id: props.user.id,
      name: props.user.name,
      bio: props.user.bio,
      location: props.user.location,
      website: props.user.website,
      birth: props.user.birth,
      bgImage: props.user.bg_image,
      profileImage: props.user.profile_image,
    });

    // TODO : 이미지 저장 구현
    const bgImageVal = ref(null);
    const bgImageSrc = ref(null);
    function updateBgImage(val) {
      userInfo.value.bgImage = '';

      const reader = new FileReader();
      reader.onload = function (e) {
        bgImageSrc.value = e.target.result;
      };
      reader.readAsDataURL(val);
    }

    const profileImageVal = ref(null);
    const profileImageSrc = ref(null);
    function updateProfileImage(val) {
      userInfo.value.profileImage = '';

      const reader = new FileReader();
      reader.onload = function (e) {
        profileImageSrc.value = e.target.result;
      };
      reader.readAsDataURL(val);
    }

    function saveUserInfo(userInfo) {
      const formData = new FormData();
      if (bgImageVal.value) formData.append('bgFile', bgImageVal.value);
      if (profileImageVal.value) formData.append('profileFile', profileImageVal.value);
      if (userInfo.birth === 'None') {
        formData.append("birth", '');
      } else {
        formData.append("birth", userInfo.birth);
      }

      formData.append("user_id", userInfo.user_id);
      formData.append("name", userInfo.name);
      formData.append("bio", userInfo.bio || '');
      formData.append("location", userInfo.location || '');
      formData.append("website", userInfo.website || '');
      formData.append("bg_image", userInfo.bgImage || '');
      formData.append("profile_image", userInfo.profileImage || '');

      api.post("/user", formData, { header: { "Content-Type": "multipart/form-data" }, })
        .then(() => {
          onDialogOK();
        })
        .catch((err) => {
          console.log(err);
        });
    }

    return {
      dialogRef,
      onDialogOK,
      onDialogCancel,

      bgImageVal,
      bgImageSrc,
      updateBgImage,

      profileImageVal,
      profileImageSrc,
      updateProfileImage,

      userInfo,
      saveUserInfo,
    };
  },
};
</script>

<style lang="scss">
.edit-profile-dialog {
  .q-dialog__inner {
    .q-card {
      width: 100%;
      max-height: 600px;
      padding: 50px 0 20px;
      position: relative;
      border-radius: 12px;
      .dialog-header {
        position: absolute;
        height: 50px;
        width: 100%;
        top: 0;
        left: 0;
        padding: 0 12px;
        .title {
          font-size: 20px;
          font-weight: 700;
        }
        .close-btn {
          margin-right: 12px;
        }
        .save-btn {
          height: 30px;
          position: absolute;
          top: 50%;
          transform: translateY(-50%);
          right: 12px;
        }
      }
      .q-scrollarea {
        &__container {
          .q-scrollarea__content {
            .profile-card-container {
              .photo-section {
                position: relative;
                margin-bottom: 80px;
                .bg-image {
                  position: relative;
                  .edit-bg-image {
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: rgba(0, 0, 0, 0.3);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    .q-icon {
                      position: absolute;
                      background: rgba(66, 66, 66, 0.5);
                      border-radius: 50%;
                      padding: 10px 12px 12px 11px;
                      font-size: 24px;
                    }
                    .q-field {
                      width: 100%;
                      height: 100%;
                      &__inner {
                        .q-field__control {
                          height: 100%;
                          &-container {
                            .q-field__native {
                              display: none;
                            }
                          }
                        }
                      }
                    }
                  }
                }
                .profile-image {
                  position: relative;

                  .q-avatar {
                    width: 120px;
                    height: 120px;
                    position: absolute;
                    left: 30px;
                    top: -50px;
                    background: white;
                    &__content {
                      border: 3px solid white;
                    }
                    img {
                      object-fit: cover;
                    }
                  }
                  .edit-profile-image {
                    position: absolute;
                    width: 120px;
                    height: 120px;
                    left: 30px;
                    top: -50px;
                    background: rgba(0, 0, 0, 0.3);
                    border-radius: 50%;
                    border: 3px solid white;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    .q-icon {
                      position: absolute;
                      position: absolute;
                      background: rgba(66, 66, 66, 0.5);
                      border-radius: 50%;
                      padding: 10px 12px 12px 11px;
                      font-size: 24px;
                    }
                    .q-field {
                      width: 100%;
                      height: 100%;
                      &__inner {
                        .q-field__control {
                          height: 100%;
                          border-radius: 50%;
                          &-container {
                            .q-field__native {
                              display: none;
                            }
                          }
                        }
                      }
                    }
                  }
                }
              }
              .q-form {
                padding: 12px;
                .q-field {
                  margin-bottom: 12px;
                  &:last-of-type {
                    margin-bottom: 0;
                  }
                  &__inner {
                    .q-field__control {
                      height: 56px;
                    }
                  }
                  &:nth-of-type(2) {
                    .q-field__inner {
                      .q-field__control {
                        height: 90px;
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
</style>
