import {
  BasePost,
  AdsTrendsColumn,
  StickySideSection,
  PostNameLabel,
  ReportDialog,
  SupportDialog
} from "@/views/components";
import { formMixins, errorHandling, asyncLoader } from "@/mixins";
import morphFilters from "@/filters/morphFilters";

export default {
  components: {
    BasePost,
    AdsTrendsColumn,
    StickySideSection,
    PostNameLabel,
    ReportDialog,
    SupportDialog
  },
  props: {
    slug: String
  },
  mixins: [formMixins, errorHandling, asyncLoader],
  data() {
    return {
      reportedSlug: "",
      supportSlug: "",
      tabs: "posts",
      isFollowed:
        !!this.slug &&
        this.$store.getters["profile/followingList"].includes(this.slug),
      isConnectionPending: false,
      isConnected: false,
      isContextMenuVisible: false,
      engagementsInfo: {
        following_count: 1,
        followers_count: 10,
        connections: 23
      },
      engagements: [
        {
          icon: "fas fa-users",
          name: "following_count",
          label: ["Following", "Following"]
        },
        {
          icon: "fas fa-user-friends",
          name: "follower_count",
          label: ["Follower", "Followers"]
        },
        {
          icon: "fas fa-user-plus",
          name: "connection_count",
          label: ["Connection", "Connections"]
        }
      ],
      providerInfo: [
        { name: "location", icon: "fas fa-map-marker-alt" },
        {
          name: "service_type",
          label: "type of service",
          icon: "fas fa-hand-holding-medical"
        },
        {
          name: "mobile_no",
          label: "mobile number",
          icon: "fas fa-mobile-alt"
        },
        { name: "tel_no", label: "telephone number", icon: "fas fa-phone-alt" },
        { name: "email", icon: "fas fa-envelope" },
        { name: "website", icon: "fas fa-globe" },
        { name: "tags", icon: "fas fa-search" },
        { name: "about", label: "additional information", icon: "fas fa-info" }
      ],
      regularIntroInfo: [
        { name: "location", label: "address", icon: "fas fa-map-marker-alt" },
        {
          name: "mobile_no",
          label: "mobile number",
          icon: "fas fa-mobile-alt"
        },
        { name: "tel_no", label: "telephone number", icon: "fas fa-phone-alt" },
        { name: "email", icon: "fas fa-envelope" },
        {
          name: "emergency_contact_person",
          label: "your emergency contact person",
          icon: "fas fa-address-card"
        },
        {
          name: "emergency_contact_number",
          label: "your emergency contact person's number",
          icon: "fas fa-phone-square-alt"
        }
      ],
      providerIntro: {
        location: "",
        service_type: "",
        mobile_no: "",
        tel_no: "",
        email: "",
        website: "",
        tags: [],
        about: ""
      },
      cacheProviderIntro: {},
      regularIntro: {
        location: "",
        mobile_no: "",
        tel_no: "",
        email: "",
        emergency_contact_person: "",
        emergency_contact_number: ""
      },
      cacheRegularIntro: {},
      iconOptions: [
        { label: "Default", value: "fas fa-user" },
        { label: "Star", value: "fas fa-star" },
        { label: "Heart", value: "fas fa-heart" },
        { label: "Diamond", value: "fas fa-gem" },
        { label: "Trophy", value: "fas fa-trophy" }
      ],
      colorOptions: [
        { label: "Default", value: "primary" },
        { label: "Violet", value: "accent" },
        { label: "Green", value: "positive" },
        { label: "Red", value: "negative" }
      ],
      headerData: {
        icon_name: "",
        icon_color: "",
        bio: ""
      },
      cacheHeaderData: {},
      photoURL: null,
      photo: null,
      morphFilters,
      providerInfoFields: [
        {
          key: "location",
          attrs: { type: "textarea", rows: 2, label: "Location" }
        },
        {
          key: "service_type",
          attrs: { label: "What type of mental health service do you offer?" }
        },
        { key: "mobile_no", attrs: { label: "Mobile No." } },
        { key: "tel_no", attrs: { label: "Telephone No." } },
        { key: "email", attrs: { label: "Email address" } },
        { key: "website", attrs: { label: "Website" } },
        {
          key: "tags",
          fieldType: "select",
          attrs: {
            label: "Related keywords",
            hint: "Press Enter to add tag",
            inputDebounce: "0",
            useInput: true,
            useChips: true,
            multiple: true,
            hideDropdownIcon: true,
            clearable: true
          }
        },
        {
          key: "about",
          attrs: { type: "textarea", rows: 4, label: "Additional Information" }
        }
      ],
      regularInfoFields: [
        {
          key: "location",
          attrs: { type: "textarea", rows: 2, label: "Address" }
        },

        { key: "mobile_no", attrs: { label: "Mobile No." } },
        { key: "tel_no", attrs: { label: "Telephone No." } },
        { key: "email", attrs: { label: "Email address" } },
        {
          key: "emergency_contact_person",
          attrs: { label: "Emergency Contact Person" }
        },
        {
          key: "emergency_contact_number",
          attrs: { label: "Emergency Contact Person's No." }
        }
      ],
      userProfileData: { profile: {} },
      avatarIcon: {
        regular: "fas fa-user",
        provider: "fas fa-hands-helping",
        organization: "fas fa-building"
      },
      reportReasons: [
        "Posting inappropriate things",
        "Suspicious account",
        "Violating the community guidelines",
        "Harrassment or Bullying",
        "Pretending to be someone else"
      ],
      reportData: {
        reason: "",
        description: ""
      },
      userFollowing: [],
      userFollower: [],
      userConnections: [],
      userPosts: []
    };
  },
  computed: {
    posts() {
      return this.$store.state.post.posts;
    },
    user() {
      return this.$store.state.auth.user;
    },
    userGroup() {
      return this.userProfileData.groups?.[0] || "";
    },
    ownGroup() {
      return this.$store.getters["auth/group"];
    },
    ownFollowing() {
      return this.$store.getters["profile/followingList"];
    },
    requestedConnection() {
      return this.$store.getters["profile/requestedConnectionsList"];
    },
    ownConnection() {
      return this.$store.getters["profile/connectionList"];
    },
    pendingConnection() {
      return this.$store.getters["profile/pendingConnectionsList"];
    }
  },
  methods: {
    createValue(val, done) {
      done(val.toLowerCase(), "add-unique");
    },
    editHeader() {
      const {
        icon_name = "",
        icon_color = "",
        profile = {}
      } = this.userProfileData;
      const { bio } = profile;
      if (this.ownGroup === "regular") {
        this.headerData.icon_name =
          icon_name || this.avatarIcon[this.userGroup];
        this.headerData.icon_color = icon_color || "primary";
      }
      this.headerData.bio = bio;

      this.cacheHeaderData = { ...this.headerData };

      this.$refs.editHeaderForms.showDialog();
    },
    notifyOnSave() {
      this.$q.notify({
        type: "positive",
        message: "Changes has been applied.",
        classes: "text-body1",
        position: this.$q.screen.gt.sm ? "bottom-left" : "bottom",
        icon: "fas fa-check",
        multiLine: this.$q.screen.gt.sm
      });
    },
    async updateHeaderData() {
      this.startLoading();
      const { data, success } = await this.$store.dispatch(
        "profile/updateProfileInfo",
        this.headerData
      );
      await this.timeout();
      this.stopLoading();
      if (success) {
        this.userProfileData = { ...data };
        this.$refs.editHeaderForms.cancel();
        this.notifyOnSave();
      }
    },
    editProviderInfo() {
      const { profile } = this.userProfileData;

      this.providerIntro = Object.assign({}, this.providerIntro, profile);

      this.cacheProviderIntro = { ...this.providerIntro };
      this.$refs.editProviderIntroForms.showDialog();
    },
    async updateProviderIntro() {
      this.startLoading();

      let payload = { ...this.providerIntro };
      payload.tags = JSON.stringify(payload.tags);

      const { data, success } = await this.$store.dispatch(
        "profile/updateProfileInfo",
        payload
      );
      await this.timeout();
      this.stopLoading();
      if (success) {
        this.userProfileData = { ...data };
        this.$refs.editProviderIntroForms.cancel();
        this.notifyOnSave();
      }
    },
    editRegularInfo() {
      const { profile } = this.userProfileData;

      this.regularIntro = Object.assign({}, this.regularIntro, profile);

      this.cacheRegularIntro = { ...this.regularIntro };
      this.$refs.editRegularIntroForms.showDialog();
    },
    async updateRegularIntro() {
      this.startLoading();
      const { data, success } = await this.$store.dispatch(
        "profile/updateProfileInfo",
        this.regularIntro
      );
      await this.timeout();
      this.stopLoading();
      if (success) {
        this.userProfileData = { ...data };
        this.$refs.editRegularIntroForms.cancel();
        this.notifyOnSave();
      }
    },
    fileUpload() {
      this.$refs.fileUploader.click();
    },
    async onUpload(e) {
      const file = e.target.files[0];

      this.photo = file;

      const { type, size } = this.photo;
      const allowedTypes = ["image/jpeg", "image/jpg", "image/png"];

      if (allowedTypes.includes(type) && size <= 2000000) {
        this.photoURL = URL.createObjectURL(this.photo);

        const payload = new FormData();
        payload.append("photo", this.photo);

        this.startLoading();

        const { data } = await this.$store.dispatch(
          "profile/uploadPhoto",
          payload
        );

        await this.timeout();

        this.stopLoading();
        this.userProfileData = { ...data };
      } else this.photo = this.photoURL = null;
    },
    async removePhoto() {
      this.startLoading();

      const { success } = await this.$store.dispatch("profile/removePhoto");

      await this.timeout();
      this.stopLoading();

      if (success)
        this.photo = this.photoURL = this.userProfileData.photo = null;
    },
    setContactEmail(state) {
      this.providerIntro.email = state ? this.user.username : "";
    },
    setRegularContactEmail(state) {
      this.regularIntro.email = state ? this.user.username : "";
    },

    async unfollowUser(slug) {
      await this.$store.dispatch("profile/unfollowUser", { slug });

      await this.$store.dispatch("profile/getUserFollowing", {
        ownData: true,
        slug: this.user.slug
      });

      const { data } = await this.$store.dispatch("profile/getUserProfile", {
        slug: this.userProfileData.slug
      });
      this.userProfileData = { ...data };
    },
    async followUser(slug) {
      await this.$store.dispatch("profile/followUser", { slug });

      await this.$store.dispatch("profile/getUserFollowing", {
        ownData: true,
        slug: this.user.slug
      });

      const { data } = await this.$store.dispatch("profile/getUserProfile", {
        slug: this.userProfileData.slug
      });
      this.userProfileData = { ...data };
    },
    showReportAccount() {
      this.reportData.reason = this.reportData.description = "";
      this.$refs.reportAccount.showDialog();
    },
    async reportAccount() {
      this.startLoading();

      const { data } = await this.$store.dispatch("profile/reportAccount", {
        ...this.reportData,
        slug: this.slug
      });

      await this.timeout();

      this.stopLoading();

      this.$refs.reportAccount.cancel();
      if (data)
        this.$q.notify({
          message: "Thank you for letting us know.",
          classes: "text-body1",
          position: this.$q.screen.gt.sm ? "bottom-left" : "bottom",
          icon: "fas fa-flag",
          multiLine: this.$q.screen.gt.sm
        });
    },
    async addAsConnection() {
      await this.$store.dispatch("profile/addAsConnection", {
        slug: this.slug
      });
      await this.$store.dispatch("profile/getRequestedConnections");
    },
    async removeConnectionRequest() {
      await this.$store.dispatch("profile/removeConnectionRequest", {
        slug: this.slug
      });
      await this.$store.dispatch("profile/getRequestedConnections");
    },
    async acceptConnection() {
      await this.$store.dispatch("profile/setConnectionStatus", {
        slug: this.slug,
        status: "accept"
      });

      await this.$store.dispatch("profile/getPendingConnections");
      const { data } = await this.$store.dispatch("profile/getUserProfile", {
        slug: this.slug
      });
      this.userProfileData = { ...data };

      await this.$store.dispatch("profile/getUserConnections", {
        ownData: true,
        slug: this.user.slug
      });

      const { data: userNewConnections } = await this.$store.dispatch(
        "profile/getUserConnections",
        {
          slug: this.slug
        }
      );
      this.userConnections = [...userNewConnections.items];
    },
    async denyConnection() {
      await this.$store.dispatch("profile/setConnectionStatus", {
        slug: this.slug,
        status: "deny"
      });

      await this.$store.dispatch("profile/getPendingConnections");
    },
    async removeConnection() {
      const dialogResponse = await this.$refs.removeConnection.showDialog();

      if (!dialogResponse) return;

      await this.$store.dispatch("profile/removeConnection", {
        slug: this.slug
      });

      const { data } = await this.$store.dispatch("profile/getUserProfile", {
        slug: this.slug
      });
      this.userProfileData = { ...data };

      await this.$store.dispatch("profile/getUserConnections", {
        ownData: true,
        slug: this.user.slug
      });

      const { data: userNewConnections } = await this.$store.dispatch(
        "profile/getUserConnections",
        {
          slug: this.slug
        }
      );

      this.userConnections = [...userNewConnections.items];
    },
    async deletePost(slug, index) {
      const dialogResponse = await this.$root.deletePost();

      if (!dialogResponse) return;
      const { success } = await this.$store.dispatch("post/deletePost", {
        slug
      });
      if (success) this.$delete(this.userPosts, index);
    },
    async bookmarkPost(slug, index, isSaved) {
      let action = "post/unsavePost";

      if (!isSaved) action = "post/savePost";

      const response = await this.$store.dispatch(action, {
        slug
      });

      const { success, data } = response;

      if (success) this.$set(this.userPosts, index, data);
    },
    showReportDialog(slug) {
      this.reportedSlug = slug;
      this.$refs.report.showReportDialog();
    },
    async reportPost(reportData) {
      const payload = { ...reportData, slug: this.reportedSlug };

      this.startLoading();
      const response = await this.$store.dispatch("post/reportPost", payload);
      await this.timeout();
      this.stopLoading();

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
    },
    showSupportDialog(slug) {
      this.supportSlug = slug;
      this.$refs.support.showSupportDialog();
    },
    async supportPost(supportData) {
      let payload = { ...supportData, post_slug: this.supportSlug };

      payload.slugs = JSON.stringify(payload.slugs);
      this.startLoading();
      const response = await this.$store.dispatch("post/supportPost", payload);
      await this.timeout();
      this.stopLoading();

      const { success } = response;
      if (success) {
        this.$refs.support.cancel();
        this.$q.notify({
          message: "Thank you for letting us know.",
          classes: "text-body1",
          position: this.$q.screen.gt.sm ? "bottom-left" : "bottom",
          icon: "fas fa-flag",
          multiLine: this.$q.screen.gt.sm
        });
      }
    }
  },
  watch: {
    "$route.params": {
      handler() {
        this.$router.go();
      }
    }
  },
  beforeRouteEnter(to, from, next) {
    next(async vm => {
      if (from.name === to.name) vm.$router.go();
      const slug = to.params.slug || vm.$store.state.auth.user.slug;
      const { data, success } = await vm.$store.dispatch(
        "profile/getUserProfile",
        {
          slug
        }
      );

      if (!success) {
        vm.$router.push({ name: "Profile" });
        return;
      }
      vm.userProfileData = { ...data };

      if (!to.params.slug) {
        vm.userFollowing = vm.$store.state.profile.following;
        vm.userFollower = vm.$store.state.profile.follower;
        vm.userConnections = vm.$store.state.profile.connections;
      } else {
        const { data: following } = await vm.$store.dispatch(
          "profile/getUserFollowing",
          {
            slug: to.params.slug
          }
        );
        const { data: follower } = await vm.$store.dispatch(
          "profile/getUserFollower",
          {
            slug: to.params.slug
          }
        );
        const { data: connections } = await vm.$store.dispatch(
          "profile/getUserConnections",
          {
            slug: to.params.slug
          }
        );
        vm.userFollowing = [...following.items];
        vm.userFollower = [...follower.items];
        vm.userConnections = [...connections.items];
      }
      const { data: posts } = await vm.$store.dispatch("post/getPosts", {
        qs_type: to.params.slug ? "other-profile" : "owned",
        created_by__slug: to.params.slug ? slug : ""
      });

      vm.userPosts = [...posts.items];
    });
  }
};
