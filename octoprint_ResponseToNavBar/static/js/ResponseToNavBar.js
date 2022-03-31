$(function() {
    function ResponseToNavBarViewModel(parameters) {
        var self = this;
		
		self.loginState = parameters[0];

		self.onDataUpdaterPluginMessage = function(plugin, data) {
            if (plugin != "ResponseToNavBar") {
				// console.log('Ignoring '+plugin);
                return;
            }
			
			if(data.type == "popup") {
				// console.log(data.msg);
				$("#ResponseToNavBar").text(data.msg);
			}
		}

    }

    // This is how our plugin registers itself with the application, by adding some configuration
    // information to the global variable OCTOPRINT_VIEWMODELS
    OCTOPRINT_VIEWMODELS.push([
        // This is the constructor to call for instantiating the plugin
        ResponseToNavBarViewModel,

        // This is a list of dependencies to inject into the plugin, the order which you request
        // here is the order in which the dependencies will be injected into your view model upon
        // instantiation via the parameters argument
        ["loginStateViewModel"],

        // Finally, this is the list of selectors for all elements we want this view model to be bound to.
        ["#ResponseToNavBarMenu"]
    ]);
});