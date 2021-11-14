<template>
  <div id="nochatopen">
    <img id="logo" src="@/assets/Commutify-logos_transparent.png" />
    <p>Verifying Your Account!!</p>
  </div>
</template>

<script>
export default {
  name: "VerifyUser",
  data() {
    return {
      verified: false,
    };
  },
  methods: {
    verify() {
      let email = this.$route.params.email;
      let verify_pin = this.$route.params.pin;
      console.log(email, verify_pin);
      this.axios
        .get(`auth/verify/${email}/${verify_pin}/`)
        .then(() => {
          this.verified = true;
          this.$router.push("/main/");
        })
        .catch((err) => console.log(err.response.data));
    },
  },
  created() {
    this.verify();
  },
};
</script>

<style scoped>
#nochatopen{
  background: url("../assets/nochatopen.jpg");
  background-size: cover;
  color: #fff;
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
</style>