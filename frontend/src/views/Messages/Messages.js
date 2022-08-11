import { VEmojiPicker } from "v-emoji-picker";
import { request } from "@/services";
import { asyncLoader, formMixins } from "@/mixins";

export default {
  components: {
    VEmojiPicker
  },
  mixins: [asyncLoader, formMixins],
  data() {
    return {
      conversations: [],
      messages: [],
      leftDrawerOpen: false,
      search: "",
      message: "",
      currentConversationIndex: -1,
      avatarIcon: {
        regular: "fas fa-user",
        provider: "fas fa-hands-helping",
        organization: "fas fa-building"
      },
      chatSocket: null,
      isReady: false,
      slug: ""
    };
  },
  computed: {
    currentConversation() {
      return this.currentConversationIndex < 0 ? {} : this.conversations[0];
    },
    style() {
      return { height: this.$q.screen.height + "px" };
    },
    user() {
      return this.$store.state.auth.user;
    }
  },
  methods: {
    sendMessage() {
      if (!this.message) return;
      this.chatSocket.send(
        JSON.stringify({
          message: this.message,
          sender: this.user.slug
        })
      );
      let vm = this;
      this.chatSocket.onmessage = function(e) {
        vm.messages.push(JSON.parse(e.data));

        vm.scroll();
      };

      this.message = "";
    },
    scroll() {
      this.$nextTick(() => {
        this.$refs.chatbox.scrollTop = this.$refs.chatbox.scrollHeight;
      });
    },
    initWS(slug) {
      let path = `ws://${window.location.hostname}:8080/ws/chat/message/${slug}/`;
      this.chatSocket = new WebSocket(path);
      this.startLoading();
      this.chatSocket.onopen = function() {};
    },
    async selectCurrentConversation(index) {
      this.currentConversationIndex = index;

      this.initWS(this.currentConversation.slug);

      const response = await request("chat/messages/", {
        filter: JSON.stringify({
          chatroom__slug: this.currentConversation.slug
        })
      });
      this.messages = [...response.data.items];
      this.scroll();
      this.stopLoading();
    }
  },
  async mounted() {
    this.startLoading();
    const { data: rooms } = await request("chat/rooms/");

    this.conversations = [...rooms.items];

    if (this.slug) {
      const { success, data } = await request("chat/room/get/", {
        user_slugs: JSON.stringify([this.slug])
      });

      if (success) {
        const listRooms = this.conversations.map(room => room.slug);
        if (!listRooms.includes(data.slug)) this.conversations.push(data);
      }
    }

    this.stopLoading();
  },
  watch: {
    "$route.query": {
      immediate: true,
      deep: true,
      handler(nv) {
        this.slug = nv.slug;
      }
    }
  }
};
