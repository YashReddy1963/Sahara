import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';
import { Link } from 'react-router-dom';

export function Nav(){
  return (
    <Navbar className="bg-black opacity-95">
      <Container>
        <Navbar.Brand className='text-white font-serif text-5xl left-[6%] relative cursor-pointer flex'>
            <img src="./img/sahara.png" alt="saharalogo" className='mr-4chat'/>सहारा</Navbar.Brand>
        <Navbar.Toggle />
        <div className="justify-content-end">
          <button className='text-black bg-white p-1 rounded-full text-lg w-32 font-normal'>
            <Link to="/sign-up">Get Started</Link>
            
          </button>
        </div>
      </Container>
    </Navbar>
  );
}

export default Nav;