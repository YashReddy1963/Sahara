import React, { useState } from "react";
import axios from "axios";

const DonateForm = ({ selectedPost, onClose }) => {
  const [donorName, setDonorName] = useState("");
  const [amount, setAmount] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!amount || !donorName) {
      alert("Please fill in all required fields.");
      return;
    }

    const donationData = {
      donor_username: donorName,
      fund_post_title: selectedPost.title,
      amount: amount,
      transaction_id: `TXN-${Date.now()}`, // Generate a unique transaction ID
    };

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/api/donate/", // Change to your API endpoint
        donationData,
        { headers: { "Content-Type": "application/json" } }
      );

      alert("Donation successful!");
      onClose(); // Close the form after donation
    } catch (error) {
      console.error("Donation failed:", error.response?.data || error.message);
      alert("Donation failed. Please try again.");
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center">
      <div className="bg-white p-6 rounded-lg shadow-lg w-96">
        <h2 className="text-xl font-bold mb-4">Donate to {selectedPost.ngo_name}</h2>
        <p className="text-gray-700 mb-2">Title: {selectedPost.title}</p>

        <form onSubmit={handleSubmit} className="flex flex-col space-y-3">
          <input
            type="text"
            placeholder="Your Name"
            value={donorName}
            onChange={(e) => setDonorName(e.target.value)}
            className="border p-2 rounded"
            required
          />
          <input
            type="number"
            placeholder="Amount (₹)"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            className="border p-2 rounded"
            required
          />
          <button type="submit" className="bg-blue-500 text-white py-2 rounded">
            Donate
          </button>
          <button type="button" onClick={onClose} className="text-red-500">
            Cancel
          </button>
        </form>
      </div>
    </div>
  );
};

export default DonateForm;
