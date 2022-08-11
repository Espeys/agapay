import router from "@/router";
import { request } from "@/services";

export default {
  namespaced: true,
  state: {
    token: localStorage.getItem("accessToken") || "",
    user: {}
  },
  getters: {
    isAuthenticated: state => !!state.token,
    group: state => state.user?.groups?.[0] || "",
    userID: state => state.user?.slug || ""
  },
  mutations: {
    SET_CREDENTIALS: (state, { token, user }) => {
      state.token = token;
      state.user = Object.assign({}, state.user, user);
    },
    DELETE_TOKEN: state => (state.token = ""),
    DELETE_USER: state => (state.user = Object.assign({})),
    SET_USER: (state, payload) =>
      (state.user = Object.assign({}, state.user, payload))
  },
  actions: {
    setTokenStorage({ commit }, payload) {
      const { access, refresh, user, expires, isRefresh = false } = payload,
        { groups, is_dark_mode, is_anonymous } = user;

      if (!isRefresh) commit("SET_CREDENTIALS", { token: access, user });

      localStorage.setItem("accessToken", access);
      localStorage.setItem("refreshToken", refresh);
      localStorage.setItem("expiresIn", expires);
      localStorage.setItem("user", JSON.stringify(groups));
      localStorage.setItem("darkMode", is_dark_mode);
      localStorage.setItem("anonymous", is_anonymous);
    },
    destroyUserCredentials({ commit, dispatch }) {
      commit("DELETE_TOKEN");
      localStorage.removeItem("accessToken");
      localStorage.removeItem("refreshToken");
      localStorage.removeItem("expiresIn");
      localStorage.removeItem("user");
      localStorage.removeItem("refresh");
      localStorage.setItem("darkMode", false);
      localStorage.removeItem("anonymous");
      sessionStorage.removeItem("refresh");
      dispatch("profile/deleteEngagementData", null, { root: true });
    },
    async login({ dispatch }, payload) {
      const accessToken = localStorage.getItem("accessToken");

      if (accessToken) {
        router.go();
        return;
      }

      const response = await request("accounts/login/", payload);
      const { success, data } = response;

      if (success)
        if (data.user.groups.length) dispatch("setTokenStorage", data);

      return response;
    },
    async setAccess({ dispatch }) {
      const { success, data } = await request("accounts/access/");

      if (success && data.user.groups.length) {
        dispatch("setTokenStorage", data);
        return data.user;
      }

      dispatch("destroyUserCredentials");
      router.replace({ name: "Home" });
    },
    async setRefreshToken({ dispatch }) {
      const refreshToken = localStorage.getItem("refreshToken");
      const response = await request("accounts/refresh/", {
        refresh_token: refreshToken
      });
      const { success, data } = response;
      if (success && data.user.groups.length) {
        dispatch("setTokenStorage", { ...data, isRefresh: true });
        return data.user;
      }
      dispatch("destroyUserCredentials");
      router.replace({ name: "Home" });
    },
    logout({ dispatch }) {
      dispatch("destroyUserCredentials");
      router.replace({ name: "Home" }).catch(() => {});
      router.go();
    },
    async signup({ dispatch }, payload) {
      const accessToken = localStorage.getItem("accessToken");

      if (accessToken) {
        router.go();
        return;
      }
      const response = await request("accounts/register/", payload);
      const { success, data } = response;

      if (success) dispatch("setTokenStorage", data);

      return response;
    },
    async verifyEmail(_, payload) {
      return await request("accounts/verify/email/", payload);
    },
    async retrieveAccount(_, payload) {
      return await request("accounts/password/forgot/", payload);
    },
    async changePassword(_, payload) {
      return await request("accounts/password/change/", payload);
    },
    async updateProfileConfig({ commit }, payload) {
      const response = await request("accounts/profile/config/", payload);
      const { success, data } = response;

      if (success) commit("SET_USER", data);

      return response;
    }
  }
};
