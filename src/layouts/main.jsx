import { Link } from "react-router-dom";
import { Nav }from "@/pages/auth";

export function Main(){
    return (
        <>
        <div className="relative">
            <Nav />
            <img src="/img/mainbg.jpg" alt="mainbg" className="w-full bg-cover" />
            <div className="absolute top-[30%] left-[20%] text-white">
                <h5 className="text-9xl font-serif">Sahara</h5>
                <p className="text-2xl pl-3 mt-7 font-thin">A Helping Hand for Those in Need,</p>
                <p className="text-2xl pl-3 mt-2 font-thin">Spreading Hope and Changing Lives!</p>
                <button className="m-3 mt-5 bg-white text-black p-1 rounded-full text-lg w-32 font-medium">
                    <Link to="/sign-up">
                        SignUp
                    </Link>
                    
                </button>
            </div>
        </div>
        </>
    )
}

export default Main;