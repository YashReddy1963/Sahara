import React, { useEffect, useState } from "react";
import {
  Card,
  CardHeader,
  CardBody,
  CardFooter,
  Typography,
  Button,
} from "@material-tailwind/react";
import DonateForm from "./DonateForm"; // Import the donation form

export function Home() {
  const [fundPosts, setFundPosts] = useState([]);
  const [selectedPost, setSelectedPost] = useState(null);

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

  return (
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
              <Typography className="mt-2 font-bold">
                NGO Name: {post.ngo_name}
              </Typography>
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

      {/* Show Donation Form if a post is selected */}
      {selectedPost && <DonateForm selectedPost={selectedPost} onClose={() => setSelectedPost(null)} />}
    </div>
  );
}

export default Home;
