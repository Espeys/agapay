import { errorHandling, formMixins, asyncLoader } from "@/mixins";

export default {
  mixins: [errorHandling, formMixins, asyncLoader],
  data() {
    return {
      userTypes: [
        {
          label: "Regular User",
          value: "regular"
        },
        { label: "Service Provider (Individual)", value: "provider" },
        { label: "Service Provider (Organization)", value: "organization" }
      ],
      selectedUserType: "regular",
      specificSignupFields: {
        regular: [
          { key: "first_name", attrs: { label: "First Name" } },
          { key: "last_name", attrs: { label: "Last Name" } }
        ],
        provider: [
          { key: "first_name", attrs: { label: "First Name" } },
          { key: "last_name", attrs: { label: "Last Name" } }
        ],
        organization: [
          {
            key: "company_name",
            attrs: { label: "Name of Organization / Institution / Company" }
          }
        ]
      },
      defaultSignupFields: [
        {
          key: "username",
          attrs: { type: "email", label: "Email address" }
        },
        {
          key: "password",
          attrs: { type: "password", label: "Password" }
        }
      ],
      signupData: { user_type: "regular", username: "", password: "" }
    };
  },
  computed: {
    selectedSpecificFields() {
      return this.specificSignupFields[this.selectedUserType];
    }
  },

  methods: {
    async signup() {
      this.startLoading();
      const response = await this.$store.dispatch(
        "auth/signup",
        this.signupData
      );

      this.timeout();
      this.stopLoading();

      const { success } = response;
      if (!success) {
        this.checkErrors(
          this.specificSignupFields[this.selectedUserType],
          response
        );
        this.checkErrors(this.defaultSignupFields, response);
      } else this.$router.go();
    }
  },
  watch: {
    selectedUserType(newType, oldType) {
      const defaultData = { username: "", password: "" };
      const specificData = {
        regular: { first_name: "", last_name: "" },
        provider: { first_name: "", last_name: "" },
        organization: { company_name: "" }
      };

      this.signupData = {
        ...defaultData,
        ...specificData[newType],
        user_type: newType
      };
      this.resetFieldsWithError(this.defaultSignupFields);
      this.resetFieldsWithError(this.specificSignupFields[oldType]);
    }
  }
};
