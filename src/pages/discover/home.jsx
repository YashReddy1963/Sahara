import React, { useEffect, useState } from "react";
import {
  Card,
  CardHeader,
  CardBody,
  CardFooter,
  Typography,
  Button,
  Input,
} from "@material-tailwind/react";

export function Home() {
  const token = localStorage.getItem("access_token");
  const [fundPosts, setFundPosts] = useState([]);
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [selectedImage, setSelectedImage] = useState(null);
  const [formData, setFormData] = useState({
    ngo_name: "",
    title: "",
    reason: "",
    amount: "",
    image: null,
  });
  const [selectedPost, setSelectedPost] = useState(null);

  // Fetching fund posts from API
  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/fund-posts/")
      .then((response) => response.json())
      .then((data) => {
        const updatedData = data.map((post) => ({
          ...post,
          image: post.image ? `http://127.0.0.1:8000${post.image}` : null,
        }));
        setFundPosts(updatedData);
      })
      .catch((error) => console.error("Error fetching data:", error));
  }, []);

  // Handling image upload
  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      const imageUrl = URL.createObjectURL(file);
      setSelectedImage(imageUrl);
      setFormData({ ...formData, image: file }); // Store file in formData
    }
  };

  // Handling form input change
  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // Handling form submission
  const handleSubmit = async () => {
    if (!token) {
      alert("You must be logged in to submit a fund request.");
      return;
    }

    const formDataToSend = new FormData();
    formDataToSend.append("ngo_name", formData.ngo_name);
    formDataToSend.append("title", formData.title);
    formDataToSend.append("reason", formData.reason);
    formDataToSend.append("amount", formData.amount);
    if (formData.image) {
      formDataToSend.append("image", formData.image);
    }

    try {
      const response = await fetch("http://localhost:8000/api/fund-request/", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formDataToSend, // No need to set Content-Type manually
      });

      const data = await response.json();
      if (response.ok) {
        alert("Fund request submitted successfully!");
        setIsFormOpen(false);
        setSelectedImage(null);
        setFormData({ ngo_name: "", title: "", reason: "", amount: "", image: null });
      } else {
        alert(data.error || "Failed to submit fund request.");
      }
    } catch (error) {
      console.error("Error submitting fund request:", error);
      alert("Something went wrong!");
    }
  };

  return (
    <div className="relative">
      {/* Main Content */}
      <div className={`${isFormOpen ? "blur-sm" : ""} transition-all duration-300`}>
        <Button className="mt-5 bg-orange-600" onClick={() => setIsFormOpen(true)}>
          Apply for fund request!
        </Button>
        <div className="mt-12 flex flex-wrap gap-6 justify-center">
          {fundPosts.length > 0 ? (
            fundPosts.map((post) => (
              <Card key={post.id} className="w-96 mt-6">
                <CardHeader color="blue-gray" className="relative h-56">
                  {post.image ? (
                    <img
                      src={post.image}
                      alt={post.title}
                      className="w-full h-full object-cover"
                    />
                  ) : (
                    <div className="w-full h-full flex items-center justify-center bg-gray-200 text-gray-600">
                      No Image Available
                    </div>
                  )}
                </CardHeader>
                <CardBody>
                  <Typography variant="h5" color="blue-gray" className="mb-2">
                    {post.title}
                  </Typography>
                  <Typography>{post.description}</Typography>
                  <Typography className="mt-2 font-bold">NGO Name: {post.ngo_name}</Typography>
                  <Typography>Target Amount: ₹{post.target_amount}</Typography>
                  <Typography>Collected Amount: ₹{post.collected_amount}</Typography>
                </CardBody>
                <CardFooter className="pt-0">
                  <Button onClick={() => setSelectedPost(post)}>Donate</Button>
                </CardFooter>
              </Card>
            ))
          ) : (
            <Typography>Loading...</Typography>
          )}
        </div>
      </div>

      {/* Fund Request Form Modal */}
      {isFormOpen && (
        <div className="fixed inset-0 flex items-center justify-center bg-opacity-50 bg-gray-900">
          <Card className="w-96 bg-white p-6 shadow-lg">
            <CardHeader variant="gradient" color="gray" className="mb-4 grid h-16 mt-3 bg-orange-600 place-items-center">
              <Typography variant="h3" color="white">Apply for Fund</Typography>
            </CardHeader>
            <CardBody className="flex flex-col gap-4">
              <Input label="NGO Name" size="lg" name="ngo_name" onChange={handleInputChange} value={formData.ngo_name} />
              <Input label="Title" size="lg" name="title" onChange={handleInputChange} value={formData.title} />
              <Input label="Reason" size="lg" name="reason" onChange={handleInputChange} value={formData.reason} />
              <Input label="Amount" size="lg" name="amount" type="number" onChange={handleInputChange} value={formData.amount} />

              <div>
                <label className="block text-sm font-medium text-gray-700">Upload Image</label>
                <input type="file" accept="image/*" onChange={handleImageUpload} className="mt-1 block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:outline-none" />
                {selectedImage && (
                  <div className="mt-3">
                    <Typography variant="small" color="blue-gray">Image Preview:</Typography>
                    <img src={selectedImage} alt="Selected" className="mt-2 w-full h-40 object-cover rounded-lg border" />
                  </div>
                )}
              </div>
            </CardBody>
            <CardFooter className="pt-0">
              <Button variant="gradient" fullWidth onClick={handleSubmit}>Submit</Button>
              <Button variant="text" fullWidth className="mt-2 text-red-500" onClick={() => { setIsFormOpen(false); setSelectedImage(null); }}>Close</Button>
            </CardFooter>
          </Card>
        </div>
      )}

     </div>
  );
}

export default Home;
