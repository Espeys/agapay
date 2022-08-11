import { request } from "@/services";

export default {
  namespaced: true,
  state: {
    follower: [],
    following: [],
    connections: [],
    requestedConnections: [],
    pendingConnections: []
  },
  getters: {
    followingList: state => state.following.map(user => user.slug),
    requestedConnectionsList: state =>
      state.requestedConnections.map(user => user.user.slug),
    pendingConnectionsList: state =>
      state.pendingConnections.map(user => user.user.slug),
    connectionList: state => state.connections.map(user => user.user.slug)
  },
  mutations: {
    SET_FOLLOWERS: (state, payload) => (state.follower = [...payload]),
    SET_FOLLOWING: (state, payload) => (state.following = [...payload]),
    SET_CONNECTIONS: (state, payload) => (state.connections = [...payload]),
    SET_REQUESTED_CONNECTIONS: (state, payload) =>
      (state.requestedConnections = [...payload]),
    SET_PENDING_CONNECTIONS: (state, payload) =>
      (state.pendingConnections = [...payload])
  },
  actions: {
    async getUserProfile(_, payload) {
      return await request("accounts/profile/", payload);
    },
    async updateProfileInfo({ commit }, payload) {
      const response = await request("accounts/profile/update/", payload);

      const { profile, ...user } = response.data;

      commit("auth/SET_USER", user, { root: true });

      return response;
    },
    async uploadPhoto({ commit }, payload) {
      const response = await request("accounts/profile/photo/upload/", payload);

      const { profile, ...user } = response.data;

      commit("auth/SET_USER", user, { root: true });

      return response;
    },
    async removePhoto({ commit, rootState }) {
      const response = await request("accounts/profile/photo/remove/");

      const { success } = response;
      let user = { ...rootState.auth.user };

      if (success) user.photo = "";

      commit("auth/SET_USER", user, { root: true });

      return response;
    },
    deleteEngagementData({ commit }) {
      commit("SET_FOLLOWERS", []);
      commit("SET_FOLLOWING", []);
      commit("SET_CONNECTIONS", []);
    },
    async reportAccount(_, payload) {
      return await request("accounts/profile/report/", payload);
    },
    async followUser(_, payload) {
      return await request("accounts/profile/follow/", payload);
    },
    async unfollowUser(_, payload) {
      return await request("accounts/profile/unfollow/", payload);
    },
    async getUserFollower({ commit }, payload) {
      const { ownData = false, slug } = payload;
      const response = await request(`accounts/profile/follower/${slug}/`);

      const { data } = response;
      if (ownData) commit("SET_FOLLOWERS", data.items);

      return response;
    },
    async getUserFollowing({ commit }, payload) {
      const { ownData = false, slug } = payload;
      const response = await request(`accounts/profile/following/${slug}/`);

      const { data } = response;
      if (ownData) commit("SET_FOLLOWING", data.items);

      return response;
    },
    async getUserConnections({ commit }, payload) {
      const { ownData = false, slug } = payload;
      const response = await request(`accounts/connections/accepted/${slug}/`);

      const { data } = response;
      if (ownData) commit("SET_CONNECTIONS", data.items);

      return response;
    },
    async getRequestedConnections({ commit }) {
      const response = await request(`accounts/connections/requests/`);

      const { data } = response;

      commit("SET_REQUESTED_CONNECTIONS", data.items);

      return response;
    },
    async getPendingConnections({ commit }) {
      const response = await request(`accounts/connections/pending/`);

      const { data } = response;

      commit("SET_PENDING_CONNECTIONS", data.items);

      return response;
    },
    async addAsConnection(_, payload) {
      return await request("accounts/connection/request/", payload);
    },
    async removeConnectionRequest(_, payload) {
      return await request("accounts/connections/request/deny/", payload);
    },
    async setConnectionStatus(_, payload) {
      return await request("accounts/connection/status/", payload);
    },
    async removeConnection(_, payload) {
      return await request("accounts/connection/remove/", payload);
    }
  }
};
