import axios from "axios";

const baseURL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export const uploadPDF = async (formData: FormData) => {
  try {
    const response = await axios.post(`${baseURL}/upload_doc`, formData, {
      withCredentials: true,
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    return response.data;
  } catch (error) {
    console.error("Upload failed:", error);
    throw error;
  }
};
