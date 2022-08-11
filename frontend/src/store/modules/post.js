import { request } from "@/services";

export default {
  namespaced: true,
  state: {
    supports: []
  },
  actions: {
    async createPost(_, payload) {
      const response = await request("posts/add/", payload);
      return response;
    },
    async deletePost(_, payload) {
      return await request("posts/delete/", payload);
    },
    async getPosts(_, payload) {
      return await request("posts/newsfeed/", payload);
    },
    async getPostComments(_, slug) {
      return await request(`posts/comments/${slug}/`);
    },
    async addComment(_, payload) {
      return await request("posts/comment/add/", payload);
    },
    async deleteComment(_, payload) {
      return await request("posts/comment/delete/", payload);
    },
    async likePost(_, payload) {
      return await request("posts/like/", payload);
    },
    async unlikePost(_, payload) {
      return await request("posts/unlike/", payload);
    },
    async sharePost(_, payload) {
      return await request("posts/share/", payload);
    },
    async deletePost(_, payload) {
      return await request("posts/delete/", payload);
    },
    async savePost(_, payload) {
      return await request("posts/bookmark/", payload);
    },
    async unsavePost(_, payload) {
      return await request("posts/unbookmark/", payload);
    },
    async reportPost(_, payload) {
      return await request("posts/report/", payload);
    },
    async supportPost(_, payload) {
      return await request("posts/support/send/", payload);
    },
    async reportComment(_, payload) {
      return await request("posts/comment/report/", payload);
    },
    async viewSupports(_, payload) {
      const response = await request("posts/supports/", payload);

      return response;
    },
    async acceptSupport(_, payload) {
      return await request("posts/support/accept/", payload);
    },
    async denySupport(_, payload) {
      return await request("posts/support/decline/", payload);
    }
  }
};
