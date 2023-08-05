# ApricateIO-Wrapper  

A basic python wrapper around the Apricate.io API.

---

## Example Usage

    from apricatewrapper import ApricateAPI

    api = ApricateAPI()
    
    user_res = api.users.create_user("my_user")
    token = user_res["data"]["token"]
    
    api.set_token(token)
    plots_res = api.plots.my_plots()
    print(plot_res)