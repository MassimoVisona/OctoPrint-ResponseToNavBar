# -*- coding: utf-8 -*-

import octoprint.plugin
import octoprint.settings
import string

class ResponseToNavBar(octoprint.plugin.StartupPlugin,
			octoprint.plugin.AssetPlugin,
			octoprint.plugin.TemplatePlugin,
			octoprint.plugin.SettingsPlugin):

	def AlertResponse(self, comm, line, *args, **kwargs):
		if line and line.startswith(self.filter):
			line = line.replace(self.filter,"")
			self._plugin_manager.send_plugin_message(self._identifier, dict(type="popup", msg=line))
		return line

	def on_after_startup(self):
		self.filter = self._settings.get(["filter"])
		self._logger.info("Filter: %s)" % self.filter)
						
	def get_settings_defaults(self):
		return dict(filter="")

	def on_settings_save(self, data):
		octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
		self.filter = self._settings.get(["filter"])

	def get_template_configs(self):
		return [
			dict(type="navbar", custom_bindings=False),
			dict(type="settings", custom_bindings=False)
		]

	def get_assets(self):
		return dict(js=["js/ResponseToNavBar.js"])


	def get_version(self):
		return self._plugin_version
		
	##~~ Softwareupdate hook
	def get_update_information(self):
		return dict(
			ResponseToNavBar=dict(
				displayName="ResponseToNavBar",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="MassimoVisona",
				repo="OctoPrint-ResponseToNavBar",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/MassimoVisona/OctoPrint-ResponseToNavBar/archive/{target_version}.zip"
			)
		)

__plugin_name__ = "ResponseToNavBar"
__plugin_pythoncompat__ = ">=2.7,<4"

def __plugin_load__():
	global _plugin
	global __plugin_hooks__
	global __plugin_implementation__
	__plugin_implementation__ = ResponseToNavBar()

	__plugin_hooks__ = {
		"octoprint.comm.protocol.gcode.received": __plugin_implementation__.AlertResponse,
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}
