import FormData from "form-data";
import fs from "fs";
import axios from "axios";

export default async function handler(req, res) {
  const formData = new FormData();
  formData.append(
    "file",
    fs.createReadStream(
      "/Users/aryan/Downloads/Signable-node.js/app/public/example.pdf"
    )
  );

  const response = await axios.post(
    "https://api.meaningcloud.com/summarization-1.0",
    {
      doc: { formData },
    },
    {
      params: {
        key: process.env.SUMMARIZE_API_KEY,
        url: "https://firebasestorage.googleapis.com/v0/b/house-site-bbb7a.appspot.com/o/World_Wide_Corp_lorem.pdf?alt=media&token=815a4a1c-33ae-44dd-abed-a3395b05504f",
        sentences: "5",
      },
      headers: {
        "cache-control": "no-cache",
        "Content-Type": "application/x-www-form-urlencoded",
        "content-type":
          "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
      },
    }
  );

  res.status(200).json({ data: response.data });
}
