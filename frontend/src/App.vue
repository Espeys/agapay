<template>
  <router-view />
</template>

<script>
export default {
  created() {
    const darkMode = localStorage.getItem("darkMode") === "true";

    if (darkMode) this.$q.dark.set(darkMode);
    else localStorage.setItem("darkMode", false);

    window.addEventListener("storage", rs => {
      if (
        (rs.oldValue && !rs.newValue && rs.key === "accessToken") ||
        (rs.oldValue && !rs.newValue && rs.key === "user") ||
        (rs.oldValue && !rs.newValue && rs.key === "expiresIn") ||
        (rs.oldValue && !rs.newValue && rs.key === "refreshToken")
      ) {
        if (this.$store.getters["auth/isAuthenticated"]) {
          // this.$store.dispatch("forms/disableFormEditing");
          this.$store.dispatch("auth/logout");
        }
      }
      if (
        (!rs.oldValue && rs.newValue && rs.key === "accessToken") ||
        (!rs.oldValue && rs.newValue && rs.key === "user") ||
        (!rs.oldValue && rs.newValue && rs.key === "expiresIn") ||
        (!rs.oldValue && rs.newValue && rs.key === "refreshToken")
      ) {
        if (!this.$store.getters["auth/isAuthenticated"]) this.$router.go();
      }
    });
  },
  beforeDestroy() {
    window.removeEventListener("storage", () => {});
  }
};
</script>

<style>
.link-text:hover,
.text-underline {
  text-decoration: underline;
}
.sticky {
  position: -webkit-sticky;
  position: sticky;
}
a {
  color: inherit;
  text-decoration: inherit;
}
/* or hide fullscreen button at low resolution */
.fslightbox-toolbar-button:nth-child(1) {
  display: none;
}
</style>
