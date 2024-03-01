<template>
  <q-page class="flex flex-center q-mx-auto sign-up-result-page">
    <q-card dense class="full-width">
      <q-card-section>
        <div class="text-h5 text-weight-bold text-center q-mb-xl">가입을 환영합니다;-)</div>
        <q-btn
          rounded
          color="black"
          label="로그인하러 가기"
          :to="{ name: 'SignIn' }"
        />
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script>
export default {
  name: 'SignUpResultPage',
  setup() {
    return {}
  },
}
</script>

<style lang="scss">
.sign-up-result-page {
  max-width: 400px;
  .q-card {
    padding: 12px;
    border-radius: 28px;
    .q-card__section {
      padding: 30px 16px;
      .q-btn {
        margin-top: 20px;
        width: 100%;
        height: 50px;
      }
    }
  }
}
</style>
