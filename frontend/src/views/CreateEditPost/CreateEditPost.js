import { VEmojiPicker } from "v-emoji-picker";
import FsLightbox from "fslightbox-vue";
import { VueFeedbackReaction } from "vue-feedback-reaction";
import {
  BasePost,
  AdsTrendsColumn,
  StickySideSection
} from "@/views/components";
import store from "@/store";
import { formMixins, asyncLoader } from "@/mixins";

export default {
  mixins: [formMixins, asyncLoader],
  components: {
    VEmojiPicker,
    FsLightbox,
    BasePost,
    AdsTrendsColumn,
    StickySideSection,
    VueFeedbackReaction
  },
  data() {
    return {
      type: "status",
      postContent: "",
      tags: [],
      isSensitiveContent: false,
      showImage: false,
      uploadedPhoto: null,
      uploadedPhotoURL: "",
      promotionType: "service",
      promotionOptions: [
        { label: "Campaign", value: "campaign" },
        { label: "Event", value: "event" },
        { label: "Hotline", value: "hotline" },
        { label: "Mental Health Service", value: "service" },
        { label: "Support Group", value: "group" },
        { label: "Initiative", value: "initiative" },
        { label: "Article", value: "article" },
        { label: "Advertisement", value: "ads" },
        { label: "Others", value: "other" }
      ],
      helpType: "services",
      helpOptions: [
        { label: "Goods", value: "goods" },
        { label: "Time", value: "time" },
        { label: "Services", value: "services" },
        { label: "Information", value: "information" },
        { label: "Others", value: "others" }
      ],
      sharedPost: {},
      sharedPostSlug: "",
      feedback: "",
      labels: ["Angry", "Sad", "Meh", "Satisfied", "Happy"]
    };
  },
  computed: {
    user() {
      return this.$store.state.auth.user;
    },
    group() {
      return this.$store.getters["auth/group"];
    },
    isRegularUser() {
      return this.$store.getters["auth/group"] === "regular";
    },
    filteredPostTypes() {
      const typeOptions = [
        {
          label: "Status",
          value: "status",
          description: "Share a post on News Feed",
          icon: "fas fa-edit"
        },
        {
          label: "Promotion",
          value: "promotion",
          description: "Adverties the product and services that you can offer",
          icon: "fas fa-bullhorn"
        },
        {
          label: "Diary",
          value: "diary",
          description: "Write about your personal experiences privately",
          icon: "fas fa-feather-alt"
        },
        {
          label: "Requesting help",
          value: "request",
          description: "Create a post in times you need assistance",
          icon: "fas fa-hands-helping"
        },
        {
          label: "Offering help",
          value: "offer",
          description:
            "Promote any help or assistance you can offer to your community",
          icon: "fas fa-hand-holding-medical"
        }
      ];

      let filteredOption = null;

      if (this.isRegularUser) {
        filteredOption = typeOptions.filter(type => type.value !== "promotion");
        if (this.sharedPostSlug)
          filteredOption = filteredOption.filter(
            type => type.value !== "diary"
          );
      } else
        filteredOption = typeOptions.filter(type => type.value !== "diary");

      return filteredOption;
    }
  },
  methods: {
    createValue(val, done) {
      done(val.toLowerCase(), "add-unique");
    },
    fileUpload() {
      this.$refs.fileUploader.click();
    },
    onUpload(e) {
      const file = e.target.files[0];

      this.uploadedPhoto = file;

      const { type, size } = this.uploadedPhoto;
      const allowedTypes = ["image/jpeg", "image/jpg", "image/png"];

      if (allowedTypes.includes(type) && size <= 2000000)
        this.uploadedPhotoURL = URL.createObjectURL(this.uploadedPhoto);
      else this.uploadedPhoto = null;
    },
    async createPost() {
      let payload = {
        description: this.postContent,
        item_type: this.type
      };

      if (this.type !== "diary") {
        if (this.group === "regular")
          this.$set(payload, "is_anonymous", this.user.is_anonymous);

        this.$set(
          payload,
          "tags",
          this.tags.length ? JSON.stringify(this.tags) : "[]"
        );
        this.$set(payload, "censorship", this.isSensitiveContent);
      }

      if (this.type === "promotion")
        this.$set(payload, "promotion_type", this.promotionType);
      else if (this.type === "offer")
        this.$set(payload, "help_type", this.helpType);
      else if (this.type === "request")
        this.$set(payload, "help_type", this.helpType);
      else if (this.type === "diary")
        this.$set(
          payload,
          "mood_type",
          this.labels[this.feedback - 1].toLowerCase()
        );

      let endpoint = "post/createPost";

      if (this.sharedPostSlug) {
        this.$set(payload, "slug", this.sharedPostSlug);
        endpoint = "post/sharePost";
      }

      if (this.uploadedPhoto) {
        const fd = new FormData();
        for (const field in payload) {
          fd.append(field, payload[field]);
        }

        fd.append("banner", this.uploadedPhoto);

        payload = fd;
      }

      this.startLoading();
      const response = await this.$store.dispatch(endpoint, payload);
      const { success, data } = response;

      await this.timeout();

      this.stopLoading();

      if (success) {
        const { slug } = data;
        if (this.type === "diary") this.$router.push({ name: "Mood Tracking" });
        else this.$router.push({ name: "Post Details", params: { slug } });
      }
    }
  },
  mounted() {
    const { shared = "", type = "status" } = this.$route.query;
    this.sharedPostSlug = shared;

    const userOptions = this.filteredPostTypes.map(option => option.value);
    if (!userOptions.includes(type)) {
      this.$router.push({ name: "Post Creation" });
      return;
    }

    this.type = type;
  },
  async beforeRouteEnter(to, from, next) {
    const { data, success } = await store.dispatch("post/getPosts", {
      slug: to.query.shared
    });

    if (!success) {
      next({ name: "Post Creation" });
      return;
    }

    next(vm => {
      vm.sharedPost = { ...data };
    });
  },
  watch: {
    tags(nv) {
      if (nv.length > 5) {
        this.$nextTick(() => {
          this.tags.pop();
        });
      }
    }
  }
};
