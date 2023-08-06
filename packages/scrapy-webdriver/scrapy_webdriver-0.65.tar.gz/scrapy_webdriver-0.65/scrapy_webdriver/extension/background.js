
                function callbackFn(details) {
                    return {
                        authCredentials: {
                            username: "hbhoiqfd-1",
                            password: "uld8v8yp9d5m"
                        }
                    };
                }
                
                browser.webRequest.onAuthRequired.addListener(
                        callbackFn,
                        {urls: ["<all_urls>"]},
                        ['blocking']
                );
               