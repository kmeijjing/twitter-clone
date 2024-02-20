<template>
  <q-layout>
    <q-page-container>
      <q-page class="flex flex-center q-mx-auto sign-up-page">
        <q-card flat dense class="full-width">
          <q-card-section>
            <div class="text-h5 text-weight-bold q-mb-xl">Sign Up</div>
            <q-form @submit="signUp" class="full-width q-gutter-y-md">
              <div class="input-container">
                <div class="label">* Email</div>
                <q-input
                  type="text"
                  v-model="signupInfo.email"
                  rounded
                  outlined
                  placeholder="Your Email"
                  autofocus
                />
              </div>
              <div class="input-container">
                <div class="label">* Name</div>
                <q-input
                  type="text"
                  v-model="signupInfo.name"
                  rounded
                  outlined
                  placeholder="Your Name"
                />
              </div>
              <div class="input-container">
                <div class="label">* Password</div>
                <q-input
                  type="password"
                  v-model="signupInfo.password"
                  rounded
                  outlined
                  placeholder="Your Password"
                />
              </div>
              <div class="input-container">
                <div class="label">* Confirm Password</div>
                <q-input
                  type="password"
                  v-model="signupInfo.retypePassword"
                  rounded
                  outlined
                  placeholder="Your Confirm Password"
                />
              </div>
              <q-btn
                type="submit"
                rounded
                color="black"
                label="Sign up"
                :disable="
                  !signupInfo.email ||
                  !signupInfo.name ||
                  !signupInfo.password ||
                  !signupInfo.retypePassword
                "
              />
            </q-form>
          </q-card-section>
        </q-card>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent, ref } from 'vue'

export default defineComponent({
  name: 'SignUpPage',
  setup() {
    const signupInfo = ref({
      email: "",
      name: "",
      password: "",
      retypePassword: "",
    });

    function signUp() {
      if (signupInfo.value.password === signupInfo.value.retypePassword) {
        onDialogOK(signupInfo.value);
      } else {
        Notify.create({
          classes: "toast-message",
          message: "비밀번호를 확인해주세요.",
          color: "negative",
          position: "bottom",
        });
      }
    }
    return {
      signupInfo,
      signUp,
    }

  },
})
</script>

<style lang="scss">
.sign-up-page {
  max-width: 400px;
  .q-card {
    background: $grey-2;
    padding: 12px;
    border-radius: 28px;
    .q-card__section {
      background: white;
      padding: 30px 16px;
      .q-form {
        .q-btn {
          margin-top: 20px;
          width: 100%;
          height: 50px;
        }
      }
    }
  }
}
</style>
