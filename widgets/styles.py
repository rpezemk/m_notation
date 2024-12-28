style = """
            QWidget {
                background-color: black;
                color: #999999;
            }
            QFrame {
                background-color: black;
                color: white;
            }
            QPushButton, AsyncButton, SyncButton {
                border: 1px solid #999999;
                background-color: black;
                color: white;
                padding: 1px 12px 1px 12px;
            }
            QLabel {
                background-color: black;
                border: 1px solid white;
                padding: 5px;
            }
            QCheckBox {
                background-color: black;
                border: 1px solid white;
                padding: 5px;
                font-family: 'Courier New', monospace;
                font-size: 14px;
                spacing: 5px; 
            }
            
            QCheckBox::indicator {
                width: 14px; 
                height: 14px;
            }
            
            QCheckBox::indicator:unchecked {
                border: 2px solid gray;       
                background-color: white;         
                border-color: white white black black;           
            }
            
            QCheckBox::indicator:checked {   
                border: 2px solid green;                 
                font-size: 16px;              
                color: black;                 
                text-align: center;     
                background-color: red;        
                border-color: white white black black;  
            }
            
            QComboBox {
                background-color: black;
                color: white;
            }
            QLineEdit {
                font-family: 'Courier New', monospace;
                font-size: 14px;
                font-weight: normal;
                color: #DDDDDD;
                background-color: black;}
                
            QTextEdit {
                background-color: black;
                color: white;
            }
            
            QTableWidget {
                background-color: black;
                color: white;
                gridline-color: #555555; 
                font-family: 'Courier New';
                font-size: 12px;
            }
            
            QHeaderView::section {
                font-family: 'Courier New', monospace;
                font-size: 14px;
                color: white;
                background-color: black;
            }
            
        """