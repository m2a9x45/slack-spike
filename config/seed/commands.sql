INSERT INTO `commands` (path_id, command, workflow_id) VALUES
('open_banking', 'open-banking', 'connected-accounts'),
('easy_tranfer', 'easy-tranfer', 'easy-tranfers');
('test_test', 'wf_test', 'wf-test');
('jam_jam', 'wf_test_2', 'wf-jam');

INSERT INTO `workflows` VALUES 
('wf-test','test_test')
('wf-jam','jam_jam');

INSERT INTO `wf_steps` VALUES 
('wf-test','wf-test_step_1','button_selection','Step 1: What is the issue?'),
('wf-test','wf-test_step_2','button_selection','Step 2: Choose consent approval option'),
('wf-test','wf-test_step_3','send_message','Step 3: Workflow finished'),
('wf-jam','wf-jam_step_1','button_selection','Select a provider'),
('wf-jam','wf-jam_step_2','open_modal','test'),
('wf-jam','wf-jam_step_3','send_message','Step 4: Workflow finished');

INSERT INTO `wf_branches` VALUES 
('wf-test_step_1','wf-test_button-click-1','wf-test_step_2','Consent approval screen'),
('wf-test_step_1','wf-test_button-click-2','wf-test_step_3','Easy Transfer'),
('wf-test_step_2','wf-test_button-click-3','wf-test_step_4','Button 1'),
('wf-test_step_2','wf-test_button-click-4','wf-test_step_3','Button 2'),
('wf-test_step_2','wf-test_button-click-5','wf-test_step_3','Button 3'),
('wf-jam_step_1','wf-jam_button-click-1','wf-jam_step_2','yes'),
('wf-jam_step_2','','wf-jam_step_3','test');

INSERT INTO `wf_options` VALUES 
('wf-jam_step_2','HSBC','hsbc'),
('wf-jam_step_2','Lloyds','lloyds'),
('wf-jam_step_2','TSB','tsb');