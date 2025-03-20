import { useNavigate } from "react-router-dom";
import Nav from "../components/Navigation/Navbar.jsx";


function Home() {

    const navigate = useNavigate();

    return(
        <>
            <h1>This is the home page</h1>
            <button onClick={() => navigate('/cookingmode')} >Click to go into cooking mode</button>
        </>
    );
}

export default Home