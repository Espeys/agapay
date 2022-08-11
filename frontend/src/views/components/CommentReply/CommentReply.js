export default {
  props: {
    comment: {
      type: Object,
      required: true
    },
    reply: Boolean
  },
  data() {
    return {
      authorContextMenu: [
        {
          name: "Delete comment",
          description: "This comment will remove permanently.",
          icon: "far fa-trash-alt",
          critical: true,
          action: "delete"
        }
      ],
      audienceContextMenu: [
        {
          name: "Report comment",
          description: "I found this violating the guidelines.",
          icon: "fas fa-exclamation",
          action: "report"
        }
      ],
      isContextMenuVisible: false,
      avatarIcon: {
        regular: "fas fa-user",
        provider: "fas fa-hands-helping",
        organization: "fas fa-building"
      }
    };
  },
  computed: {
    user() {
      return this.$store.state.auth.user;
    },
    isUserAuthor() {
      return this.user?.slug === this.comment.created_by?.slug;
    },

    contextMenu() {
      return this.isUserAuthor
        ? this.authorContextMenu
        : this.audienceContextMenu;
    }
  }
};
