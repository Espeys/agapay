import { VEmojiPicker } from "v-emoji-picker";
export default {
  props: {
    user: {
      type: Object,
      required: true
    },
    value: null,
    reply: Boolean
  },
  data() {
    return {
      avatarIcon: {
        regular: "fas fa-user",
        provider: "fas fa-hands-helping",
        organization: "fas fa-building"
      }
    };
  },
  components: {
    VEmojiPicker
  }
};
