### Purpose
A PoC to provide a <u>secured</u> REST API interface on top of a dataset 

### Dataset
1. Zomato Restaurants in India 🇮🇳: [link](https://www.kaggle.com/datasets/narsingraogoud/zomato-restaurants-dataset-for-metropolitan-areas)
2. 120k rows, total size: 11 MB

### Authentication
1. Generate JWT access token by providing username & password - 
    ```
    curl -X "POST" "127.0.0.1:8000/token" -H "Content-Type: application/x-www-form-urlencoded" -d "username=john&password=secret"
    ```
2. Access a secured endpoint by sending JWT access token in request headers -
    ```
    root:
        curl -X "GET" "127.0.0.1:8000/" -H "Content-Type: application/x-www-form-urlencoded" -H "Authorization: Bearer <JWT_ACCESS_TOKEN>"
    search:
        curl -X "GET" "127.0.0.1:8000/search?dish=fish&city=hyderabad" -H "Authorization: Bearer <JWT_ACCESS_TOKEN>"
    ```
3. JWT access token is configured to expire in 3 minutes.
4. ⚠️ Ensure you use `https` - API endpoint with valid digital certificate - so that username & password passed in POST-request-body & JWT-temporary-access-token passed in request-headers are encrypted.

### Run it on local
1. Install python dependencies using `pip install -r requirements.txt`
2. Start `uvicorn` webserver 💻 -
    ```
    uvicorn main:app --reload
    ```
3. Generate JWT-temporary-access-token as mentioned above & find restaurants serving `fish` 🐠 in `Hyderabad` using -
    ```
        curl -X "GET" "127.0.0.1:8000/search?dish=fish&city=hyderabad" -H "Authorization: Bearer <JWT_ACCESS_TOKEN>"
    ```
4. Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) & [http://localhost:8000/redoc](http://localhost:8000/redoc) for documentation 📜

### Behind the scenes
1. User credentials are verified by comparing `hash(plain_password)` with `hashed_password` stored in "database - as a variable in code for testing"
2. If it succeeds, a JWT-temporary-access-token is generated using `HS256 (HMAC-SHA256)` algorithm
    - Input: payload containing username, token expiry timestamp, symmetric key
    - output: JWT-temporary-access-token
3. At this point, user is logged-in & can provide JWT-temporary-access-token in subsequent request-headers instead of username & password in every request. 
4. Imagine 2 scenarios - 1. username & password getting compromised & 2. JWT-temporary-access-token getting compromised. The 2nd scenario in better than the 1st one as JWT-temporary-access-token is temporary & may have already been expired by the time it gets into bad hands. On the other hand, username & password are permanent, unless user changes password.
5. When a user wants to access secure API endpoint, the request-headers should contain JWT-temporary-access-token
6. To verify if a JWT-temporary-access-token is valid, we extract original payload by using the same symmetric key & the same `HS256` algorithm
    - Input: JWT-temporary-access-token & symmetric key
    - Output: payload containing username, token expiry timestamp
7. A user is logged-out when JWT-temporary-access-token is expired. To login again, a user has to provide credentials (step-1) to generate another temporary JWT-temporary-access-token (step-2)

### Why `bcrypt` why not `SHA-256` for password hashing?
1. `bcrypt` performs salting which helps us defend against rainbow attacks
2. Computing power is increasing with time; we can increase the computational-cost associated with `bcrypt` hashing i.e. making it slower, which slows down brute-force attacks

### References
1. Fast API Documentation: [link](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)

