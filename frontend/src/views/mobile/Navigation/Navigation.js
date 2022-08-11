export default {
  data() {
    return {
      policies: [
        "Community Guidelines",
        "Help",
        "Safety",
        "Cookies",
        "Terms",
        "Privacy"
      ]
    };
  },
  computed: {
    activePathName() {
      const { name = "" } = this.$route;
      return name;
    },
    group() {
      return this.$store.getters["auth/group"];
    },
    userBasedMenu() {
      const menuListItem = [
        {
          name: "Promotions",
          icon: "fas fa-bullhorn",
          to: "Public Newsfeed"
        },
        {
          name: "Saved",
          icon: "fas fa-bookmark",
          to: "Saved",
          user: ["regular", "provider", "organization"]
        },
        {
          name: "Service Providers",
          icon: "fas fa-hand-holding-medical",
          to: "Service Providers"
        },
        {
          id: "accountPotManager",
          name: "Account and Promotion Manager",
          icon: "fas fa-users-cog",
          to: "Account Promotion Manager",
          user: ["provider", "organization"]
        },
        {
          name: "Connections",
          icon: "fas fa-users",
          to: "Connections",
          user: ["provider", "organization"]
        },
        {
          name: "Mood Tracking",
          icon: "fas fa-laugh",
          to: "Mood Tracking",
          user: ["regular"]
        },
        {
          name: "Psychological Self-Assessment Test",
          icon: "fas fa-shapes",
          to: "Self-Assessment Test",
          user: ["regular"]
        },
        {
          name: "Community Help",
          icon: "fas fa-hands-helping",
          to: "Community Help",
          user: ["regular", "provider", "organization"]
        },
        {
          name: "Emotional and Mental Health",
          icon: "fas fa-heart",
          to: "Emotional Mental Health",
          user: ["regular", "provider", "organization"]
        },
        {
          name: "Settings",
          icon: "fas fa-cog",
          to: "Settings",
          user: ["regular", "provider", "organization"]
        }
      ];

      return menuListItem.filter(
        menu => !menu.user || menu.user.includes(this.group)
      );
    }
  },
  methods: {
    logout() {
      this.$store.dispatch("auth/logout");
      this.$router.push({ name: "Public NewsFeed" });
      this.$router.go();
    }
  },
  watch: {
    "$q.screen": {
      deep: true,
      immediate: true,
      handler() {
        if (this.$q.screen.gt.sm) this.$router.push({ name: "Home" });
      }
    }
  }
};
