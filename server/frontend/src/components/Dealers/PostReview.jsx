import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import "./Dealers.css";
import "../assets/style.css";
import Header from '../Header/Header';

const PostReview = () => {
  const [dealer, setDealer] = useState({});
  const [review, setReview] = useState("");
  const [model, setModel] = useState("");
  const [year, setYear] = useState("");
  const [date, setDate] = useState("");
  const [carmodels, setCarmodels] = useState([]);

  const params = useParams();
  const id = params.id;

  const curr_url = window.location.href;
  const root_url = curr_url.substring(0, curr_url.indexOf("postreview"));

  const dealer_url = root_url + `djangoapp/dealer/${id}`;
  const review_url = root_url + `djangoapp/add_review`;
  const carmodels_url = root_url + `djangoapp/get_cars`;

  // Get CSRF token from browser cookies
  const getCookie = (name) => {
    let cookieValue = null;

    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");

      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();

        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(
            cookie.substring(name.length + 1)
          );
          break;
        }
      }
    }

    return cookieValue;
  };

  const postreview = async () => {
    let firstname = sessionStorage.getItem("firstname");
    let lastname = sessionStorage.getItem("lastname");
    let username = sessionStorage.getItem("username");

    let name = firstname + " " + lastname;

    // If firstname/lastname are null, use username
    if (
      !firstname ||
      !lastname ||
      firstname === "null" ||
      lastname === "null"
    ) {
      name = username;
    }

    // Validate fields
    if (
      !model ||
      review.trim() === "" ||
      date === "" ||
      year === ""
    ) {
      alert("All details are mandatory");
      return;
    }

    // Split car make and model
    const model_split = model.split(" ");

    const make_chosen = model_split[0];
    const model_chosen = model_split.slice(1).join(" ");

    const jsoninput = JSON.stringify({
      name: name,
      dealership: id,
      review: review,
      purchase: true,
      purchase_date: date,
      car_make: make_chosen,
      car_model: model_chosen,
      car_year: year
    });

    console.log(jsoninput);

    try {
      const csrfToken = getCookie("csrftoken");

      const res = await fetch(review_url, {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken
        },

        credentials: "same-origin",

        body: jsoninput
      });

      const text = await res.text();

      console.log("Response status:", res.status);
      console.log("Response:", text);

      if (!res.ok) {
        alert(
          "Failed to post review.\n\nStatus: " +
          res.status +
          "\n\n" +
          text.substring(0, 300)
        );
        return;
      }

      const json = JSON.parse(text);

      if (json.status === 200) {
        alert("Review posted successfully!");

        window.location.href =
          window.location.origin + "/dealer/" + id;
      } else {
        alert(
          json.message ||
          json.error ||
          "Review could not be posted."
        );
      }

    } catch (error) {
      console.error("Post review error:", error);
      alert("An error occurred while posting the review.");
    }
  };

  const get_dealer = async () => {
    try {
      const res = await fetch(dealer_url, {
        method: "GET",
        credentials: "same-origin"
      });

      const retobj = await res.json();

      if (retobj.status === 200) {
        setDealer(retobj.dealer);
      }
    } catch (error) {
      console.error("Error getting dealer:", error);
    }
  };

  const get_cars = async () => {
    try {
      const res = await fetch(carmodels_url, {
        method: "GET",
        credentials: "same-origin"
      });

      const retobj = await res.json();

      if (retobj.CarModels) {
        setCarmodels(retobj.CarModels);
      }
    } catch (error) {
      console.error("Error getting cars:", error);
    }
  };

  useEffect(() => {
    get_dealer();
    get_cars();
  }, []);

  return (
    <div>
      <Header />

      <div style={{ margin: "5%" }}>

        <h1 style={{ color: "darkblue" }}>
          {dealer.full_name}
        </h1>

        <textarea
          id="review"
          cols="50"
          rows="7"
          placeholder="Write your review..."
          value={review}
          onChange={(e) => setReview(e.target.value)}
        />

        <div className="input_field">
          Purchase Date{" "}
          <input
            type="date"
            value={date}
            onChange={(e) => setDate(e.target.value)}
          />
        </div>

        <div className="input_field">
          Car Make{" "}

          <select
            name="cars"
            id="cars"
            value={model}
            onChange={(e) => setModel(e.target.value)}
          >
            <option value="" disabled>
              Choose Car Make and Model
            </option>

            {carmodels.map((carmodel, index) => (
              <option
                key={index}
                value={
                  carmodel.CarMake +
                  " " +
                  carmodel.CarModel
                }
              >
                {carmodel.CarMake} {carmodel.CarModel}
              </option>
            ))}
          </select>
        </div>

        <div className="input_field">
          Car Year{" "}

          <input
            type="number"
            value={year}
            onChange={(e) => setYear(e.target.value)}
            max="2026"
            min="2015"
          />
        </div>

        <div>
          <button
            className="postreview"
            onClick={postreview}
          >
            Post Review
          </button>
        </div>

      </div>
    </div>
  );
};

export default PostReview;