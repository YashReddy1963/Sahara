import React, { useEffect, useState } from "react";
import {
  Card,
  CardHeader,
  CardBody,
  CardFooter,
  Typography,
  Button,
} from "@material-tailwind/react";

export function Home() {
  const [fundPosts, setFundPosts] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/fund-posts/")
      .then((response) => response.json())
      .then((data) => setFundPosts(data))
      .catch((error) => console.error("Error fetching data:", error));
  }, []);

  return (
    <div className="mt-12 flex flex-wrap gap-6 justify-center">
      {fundPosts.length > 0 ? (
        fundPosts.map((post) => (
          <Card key={post.id} className="w-96 mt-6">
            <CardHeader color="blue-gray" className="relative h-56">
              <img
                src={post.image}
                alt={post.title}
                className="w-full h-full object-cover"
              />
            </CardHeader>
            <CardBody>
              <Typography variant="h5" color="blue-gray" className="mb-2">
                {post.title}
              </Typography>
              <Typography>{post.description}</Typography>
              <Typography className="mt-2 font-bold">NGO Name: {post.ngo_name}</Typography>
              <Typography>Target Amount: ₹{post.target_amount}</Typography>
              Collected Amount: ₹{post.collected_amount}              
            </CardBody>
            <CardFooter className="pt-0">
              <Button>Donate</Button>
            </CardFooter>
          </Card>
        ))
      ) : (
        <Typography>Loading...</Typography>
      )}
    </div>
  );
}
export default Home;
