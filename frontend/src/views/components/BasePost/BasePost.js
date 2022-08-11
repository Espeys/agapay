import FsLightbox from "fslightbox-vue";
import { VEmojiPicker } from "v-emoji-picker";
import { VueReactionEmoji } from "vue-feedback-reaction";

import { formMixins, asyncLoader } from "@/mixins";

import {
  PostNameLabel,
  CommentField,
  CommentReply,
  BasePost
} from "@/views/components";
export default {
  name: "BasePost",
  mixins: [formMixins, asyncLoader],
  props: {
    post: Object,
    wholePost: Boolean,
    shared: Boolean,
    publicPost: Boolean
  },
  components: {
    FsLightbox,
    VEmojiPicker,
    PostNameLabel,
    CommentField,
    CommentReply,
    BasePost,
    VueReactionEmoji
  },
  data() {
    return {
      showImage: false,
      hasLiked: this.post?.is_liked || false,
      maxPreviewContent: 477,
      isContextMenuVisible: false,
      isSensitive: this.post?.censorship || false,
      authorContextMenu: [
        {
          name: "Save post",
          description: "Add this to your saved items",
          icon: "far fa-bookmark",
          separator: true,
          action: "save"
        },
        {
          name: "Delete post",
          description: "This post will remove permanently.",
          icon: "far fa-trash-alt",
          critical: true,
          action: "delete"
        }
      ],
      audienceContextMenu: [
        {
          name: "Save post",
          description: "Add this to your saved items",
          icon: "far fa-bookmark",
          separator: true,
          action: "save"
        },
        {
          name: "Find support",
          description: "I'm concerned about this post",
          icon: "far fa-flag",
          action: "support"
        },
        {
          name: "Report post",
          description: "I found this violating the guidelines",
          icon: "fas fa-exclamation",
          action: "report"
        }
      ],
      showEmojiDialog: false,
      comment: "",
      addReplyList: [],
      replies: {},
      promotionType: {
        campaign: "Campaign",
        event: "Event",
        hotline: "Hotline",
        service: "Mental Health Service",
        group: "Support Group",
        initiative: "Initiative",
        article: "Article",
        ads: "Advertisement",
        other: "Others"
      },
      postType: {
        promotion: "Promotions",
        diary: "Diary",
        request: "Requesting help",
        offer: "Offering help"
      },
      postTypeIcon: {
        promotion: "fas fa-bullhorn",
        diary: "fas fa-feather-alt",
        request: "fas fa-hands-helping",
        offer: "fas fa-hand-holding-medical"
      },
      avatarIcon: {
        regular: "fas fa-user",
        provider: "fas fa-hands-helping",
        organization: "fas fa-building"
      },
      comments: [],
      reactions: {
        angry: "hate",
        sad: "disappointed",
        meh: "natural",
        satisfied: "good",
        happy: "excellent"
      },
      reportReasons: [
        "False Information",
        "Spam",
        "Hate Speech",
        "Terrorism",
        "Harassment / Bullying",
        "Violence",
        "Racism",
        "Nudity"
      ],
      reportData: {
        reason: "",
        description: "",
        slug: ""
      }
    };
  },
  computed: {
    isAuthenticated() {
      return this.$store.getters["auth/isAuthenticated"];
    },
    truncatedContent() {
      return this.post.description.slice(0, this.maxPreviewContent);
    },
    isUserAuthor() {
      const userID = this.$store.getters["auth/userID"];
      return userID === this.post?.created_by?.slug;
    },
    user() {
      return this.$store.state.auth.user;
    },
    contextMenu() {
      return this.isUserAuthor
        ? this.authorContextMenu
        : this.audienceContextMenu;
    }
  },
  methods: {
    login() {
      this.$root.showLogin();
    },
    signup() {
      this.$root.showSignup();
    },
    selectEmoji({ data }) {
      this.comment += data;
    },
    selectReplyEmoji({ data }, slug) {
      this.replies[slug] += data;
    },
    onBannerClick() {
      if (this.wholePost) this.showImage = !this.showImage;
      else
        this.$router.push({
          name: "Post Details",
          params: { slug: this.post.slug }
        });
    },
    async addComment() {
      const { success } = await this.$store.dispatch("post/addComment", {
        description: this.comment,
        slug: this.post.slug,
        is_anonymous: this.user.is_anonymous
      });

      if (success) {
        const { data } = await this.$store.dispatch(
          "post/getPostComments",
          this.post.slug
        );
        this.comments = [...data.items];
        this.comment = "";
      }
    },
    addReply(slug) {
      if (!this.addReplyList.includes(slug)) {
        this.addReplyList.push(slug);
        this.$set(this.replies, slug, "");
      }

      this.$nextTick(() => {
        const element = document.getElementById(slug);
        element.scrollIntoView();
      });
    },
    async addCommentReply(parent_slug) {
      const response = await this.$store.dispatch("post/addComment", {
        description: this.replies[parent_slug],
        slug: this.post.slug,
        parent_slug,
        is_anonymous: this.user.is_anonymous
      });

      const { success } = response;

      if (success) {
        const { data } = await this.$store.dispatch(
          "post/getPostComments",
          this.post.slug
        );
        this.comments = [...data.items];
        this.replies[parent_slug] = "";
      }
    },
    populatePostDetails(details) {
      const { censorship, is_liked, comments } = details;

      this.comments = [...comments];
      this.hasLiked = is_liked;
      this.isSensitive = censorship;
    },
    async deleteComment(slug) {
      const dialogResponse = await this.$refs.deleteComment.showDialog();

      if (!dialogResponse) return;

      const response = await this.$store.dispatch("post/deleteComment", {
        slug
      });

      const { success } = response;

      if (success) {
        const { data } = await this.$store.dispatch(
          "post/getPostComments",
          this.post.slug
        );
        this.comments = [...data.items];
      }
    },
    async likePost() {
      const response = await this.$store.dispatch("post/likePost", {
        slug: this.post.slug
      });

      const { success, data } = response;

      if (success) this.hasLiked = data.is_liked;
    },
    async unlikePost() {
      const response = await this.$store.dispatch("post/unlikePost", {
        slug: this.post.slug
      });

      const { success, data } = response;

      if (success) this.hasLiked = data.is_liked;
    },
    showReportDialog(slug) {
      this.reportData.reason = this.reportData.description = "";
      this.reportData.slug = slug;
      this.$refs.reportComment.showDialog();
    },

    async reportComment() {
      this.startLoading();
      const response = await this.$store.dispatch(
        "post/reportComment",
        this.reportData
      );
      await this.timeout();
      this.stopLoading();

      this.$refs.reportComment.cancel();

      const { success } = response;
      if (success) {
        this.$refs.report.cancel();
        this.$q.notify({
          message: "Thank you for letting us know.",
          classes: "text-body1",
          position: this.$q.screen.gt.sm ? "bottom-left" : "bottom",
          icon: "fas fa-flag",
          multiLine: this.$q.screen.gt.sm
        });
      }
    }
  }
};
