class Checkbox:

    def __init__(self, driver, checkbox_id):
        self.checkbox_id = checkbox_id
        self.driver = driver
        self.checkbox = driver.find_element_by_id(checkbox_id)

    def get_id(self):
        return self.checkbox_id

    def is_enabled(self):
        return self.driver.execute_script("return document.getElementById('{}').checked".format(self.checkbox_id))

    def click_checkbox(self):
        if (not self.is_enabled()):
            self.checkbox.click()
    # else:
    #	print("Checkbox " + self.checkbox_id + " is already set")