export default {
  data() {
    return {
      errors: []
    };
  },
  computed: {
    fieldsWithErrors() {
      return this.errors.map(error => error["field"]);
    }
  },
  methods: {
    checkErrors(formFields, apiResponse) {
      this.errors = [...apiResponse["errors"]];

      formFields.forEach(({ key }, index) => {
        const fieldHasError = this.fieldsWithErrors.includes(key);

        if (!fieldHasError) {
          this.deleteErrorMessages(formFields, key);
          return;
        }
        const errorMessages = this.errors
          .filter(error => error["field"] === key)
          .map(error => error["message"]);

        this.$set(formFields[index], "error-message", errorMessages[0]);
      });
    },
    deleteErrorMessages(formFields, key = null) {
      const isFieldIncluded = formFields.map(field => field.key).includes(key);

      if (!isFieldIncluded) return;

      if (!key) this.$delete(formFields, "error-message");
      else {
        const index = formFields.map(field => field.key).indexOf(key);
        if (formFields[index]["error-message"])
          this.$delete(formFields[index], "error-message");
      }
    },
    resetFieldsWithError(formFields, exception = []) {
      this.fieldsWithErrors.forEach(field => {
        if (exception.includes(field)) return;
        this.deleteErrorMessages(formFields, field);
      });
    },
    showField(elementID) {
      if (!elementID) return;
      const selected = document.getElementById(elementID);
      if (!selected) return;

      selected.scrollIntoView({
        behavior: "smooth",
        block: "center",
        inline: "center"
      });
    }
  }
};
