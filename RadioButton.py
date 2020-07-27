class RadioButton:

    def __init__(self, driver, radiobutton_id):
        self.radiobutton_id = radiobutton_id
        self.driver = driver
        self.radiobutton = driver.find_element_by_id(radiobutton_id)

    def get_id(self):
        return self.radiobutton_id

    def click_radiobutton(self):
        self.radiobutton.click()