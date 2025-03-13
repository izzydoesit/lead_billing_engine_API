Steps on how to get LocalStack Pro for free (free trial sign up)
1. Signup with local stack using (possibly) throwaway email. No credit card required.
2. After sign in, fill out the rest of the form information [here](https://app.localstack.cloud/pricing/subscribe?plan=plan.hobby): ( retain the Hobby Subscription and again no credit card required).
3. Once you click on the check box for *Non Commerical Use* and *Agree with the Terms and Conditions*, the “Subscribe Now” button will be clickable. Click on it.
4. Pick up the Auth token [here](https://app.localstack.cloud/workspace/auth-tokens)
5. Open a new terminal and use the token like below:
```bash
docker run \
--rm -it \
-p 4566:4566 \
-p 4510-4559:4510-4559 \
-e LOCALSTACK_AUTH_TOKEN=<your token> \
localstack/localstack-pro
```
6. Now your localstack should be running. View the Pro services [here](https://app.localstack.cloud/inst/default/resources) 