import axios from "axios";

export default (url, data, config = null) => {
  return new Promise(resolve => {
    axios
      .post(url, data, config)
      .then(response => {
        resolve(response.data);
      })
      .catch(() => {});
  });
};
