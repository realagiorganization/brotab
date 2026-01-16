Feature: Brotab click-through demo
  As a user of the UI automation suite
  I want to click through a demo page
  So I can verify the browser is interactive

  Scenario: Increment the tab counter
    Given a demo page with a tab counter
    When I click the "Add Tab" button
    Then the counter shows "1"
