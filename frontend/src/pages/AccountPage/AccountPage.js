import { Login, Signup, ForgotPassword } from "@/views/public/views";
import { request } from "@/services";

export default {
  components: {
    Login,
    Signup,
    ForgotPassword
  },
  data() {
    return {
      search: "",
      darkMode: localStorage.getItem("darkMode") === "true",
      isMenuVisible: false,
      isNotificationVisible: false,
      isAccountMenuVisible: false,
      policies: [
        "Community Guidelines",
        "Help",
        "Safety",
        "Cookies",
        "Terms",
        "Privacy"
      ],
      headerButtons: [
        {
          icon: "fas fa-home",
          key: "home",
          label: "Home",
          to: { name: "Home" }
        },
        {
          icon: "eva-message-circle",
          key: "message",
          label: "Messages",
          to: { name: "Messages" }
        },
        { icon: "eva-bell", key: "notif", label: "Notifications" }
      ],
      tabs: ["Home", "Profile", "Messages", "Notification", "Navigation"],
      isAnonymous: localStorage.getItem("anonymous") === "true",
      isResendingEmail: false,
      avatarIcon: {
        regular: "fas fa-user",
        provider: "fas fa-hands-helping",
        organization: "fas fa-building"
      },
      notifications: []
    };
  },
  computed: {
    activePathName() {
      const { name = "" } = this.$route;
      return name;
    },
    isAuthenticated() {
      return this.$store.getters["auth/isAuthenticated"];
    },
    group() {
      return this.$store.getters["auth/group"];
    },
    userBasedMenu() {
      const menuListItem = [
        {
          id: "popular",
          name: "Promotions",
          icon: "fas fa-bullhorn",
          to: "Public Newsfeed"
        },
        {
          id: "bookmark",
          name: "Saved",
          icon: "fas fa-bookmark",
          to: "Saved",
          user: ["regular", "provider", "organization"]
        },
        {
          id: "providers",
          name: "Service Providers",
          icon: "fas fa-hand-holding-medical",
          to: "Service Providers",
          user: ["regular", "provider", "organization"]
        },
        {
          id: "connections",
          name: "Connections",
          icon: "fas fa-users",
          to: "Connections",
          user: ["provider", "organization"]
        },
        {
          id: "moodTracking",
          name: "Mood Tracking",
          icon: "fas fa-laugh",
          to: "Mood Tracking",
          user: ["regular"]
        },
        {
          id: "psat",
          name: "Psychological Self-Assessment Test",
          icon: "fas fa-shapes",
          to: "Self-Assessment Test",
          user: ["regular"]
        },
        {
          id: "communityHelp",
          name: "Community Help",
          icon: "fas fa-hands-helping",
          to: "Community Help",
          user: ["regular", "provider", "organization"]
        },
        {
          id: "emotionalMentalHealth",
          name: "Emotional and Mental Health",
          icon: "fas fa-heart",
          to: "Emotional Mental Health",
          user: ["regular", "provider", "organization"]
        }
      ];

      return menuListItem.filter(
        menu => !menu.user || menu.user.includes(this.group)
      );
    },
    user() {
      return this.$store.state.auth.user;
    }
  },
  methods: {
    async toggleDarkMode(value) {
      if (this.isAuthenticated)
        await this.$store.dispatch("auth/updateProfileConfig", {
          is_dark_mode: value
        });

      localStorage.setItem("darkMode", value);
      this.$q.dark.set(value);
    },
    async toggleAnonymous(value) {
      if (this.isAuthenticated)
        await this.$store.dispatch("auth/updateProfileConfig", {
          is_anonymous: value
        });

      localStorage.setItem("anonymous", value);
    },
    reload() {
      if (this.$route.name === "Home") {
        if (Object.keys(this.$route.query).length)
          this.$router.push({ name: "Home" });
        this.$router.go();
      }
    },
    login() {
      if (this.$q.screen.lt.md) this.isMenuVisible = false;
      this.$refs.login.showDialog();
    },
    signup() {
      if (this.$q.screen.lt.md) this.isMenuVisible = false;
      this.$refs.signup.showDialog();
    },
    switchToLogin() {
      this.$refs.signup.cancel();
      this.$refs.login.showDialog();
    },
    switchToSignup() {
      this.$refs.login.cancel();
      this.$refs.signup.showDialog();
    },
    logout() {
      this.$store.dispatch("auth/logout");
    },
    closeForgotPassword() {
      this.$refs.forgotPassword.cancel();
    },
    showForgotPassword() {
      this.$refs.login.cancel();
      this.$refs.forgotPassword.showDialog();
    },
    closeSessionExpired() {
      this.$refs.sessionExpired.cancel();
      this.$router.go();
    },
    autoRefreshTimer(threshold, interval) {
      this.refreshTimer = setInterval(() => {
        this.checkTokenDuration(threshold);
      }, interval * 60000);
    },
    checkTokenDuration(threshold) {
      const now = Date.now(),
        refresh = localStorage.getItem("refresh"),
        sessionRefresh = sessionStorage.getItem("refresh");

      if (!refresh) {
        localStorage.setItem("refresh", now);
        sessionStorage.setItem("refresh", now);
      }

      if (
        now >= this.setRefreshThreshold(threshold) &&
        refresh === sessionRefresh
      )
        this.$store.dispatch("auth/setRefreshToken");
    },
    setRefreshThreshold(minutes) {
      const expires_in = localStorage.getItem("expires_in"),
        parseDate = new Date(expires_in),
        parseDateMinutes = parseDate.getMinutes(),
        refreshThreshold = parseDate.setMinutes(parseDateMinutes - minutes);

      return refreshThreshold;
    },
    clearStorage() {
      localStorage.removeItem("refresh");
    },
    async redirect(type, slug) {
      const redirect = {
        "type-follow": {
          name: "User Profile",
          params: { slug }
        },
        "type-post": {
          name: "Post Details",
          params: { slug }
        },
        "type-connect": { name: "Connections" },
        "type-support": { name: "Connections" },
        "type-chatroom": { name: "Messages" }
      };

      if (this.$route.name === redirect[type].name) {
        this.$router.go();
        return;
      }
      this.$router.push(redirect[type]);
    },
    async queryData() {
      this.$router.push({ name: "Search", query: { keyword: this.search } });
    }
  },
  created() {
    if (this.$store.getters["auth/isAuthenticated"]) {
      const now = Date.now(),
        refresh = localStorage.getItem("refresh"),
        sessionRefresh = sessionStorage.getItem("refresh");

      if (!refresh) localStorage.setItem("refresh", now);
      if (!sessionRefresh || refresh !== sessionRefresh)
        sessionStorage.setItem("refresh", now);

      this.autoRefreshTimer(15, 3);
    }
  },
  async mounted() {
    this.$root.showLogin = this.login;
    this.$root.showSignup = this.signup;
    this.$root.showSessionExpired = this.$refs.sessionExpired.showDialog;
    this.$root.deletePost = this.$refs.deletePost.showDialog;
    if (
      (this.isAuthenticated && !this.user.is_verified) ||
      (this.isAuthenticated &&
        this.user.groups[0] !== "regular" &&
        !this.user.is_certified)
    )
      this.$refs.verificationDialog.showDialog();
    if (this.isAuthenticated) {
      const { success, data } = await request("notifications/", {
        order_values: -1
      });

      if (success) this.notifications = [...data.items];

      this.polling = setInterval(async () => {
        const { success, data } = await request("notifications/", {
          order_values: -1
        });

        if (success) this.notifications = [...data.items];
      }, 10 * 1000);
    }
  },
  beforeMount() {
    window.addEventListener("beforeunload", this.clearStorage);
  },
  beforeDestroy() {
    clearInterval(this.refreshTimer);
    clearInterval(this.polling);

    window.removeEventListener("beforeunload", this.clearStorage);
  }
};
