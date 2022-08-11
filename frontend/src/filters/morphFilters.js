const pluralize = (value, words) => words[+(+value > 1)];

const filters = {
  plural: pluralize
};
export default filters;
