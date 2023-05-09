from tkinter import *
from tkinter import messagebox
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import ast
import hashlib
import RPLCD as RPLCD
from RPLCD.gpio import CharLCD
import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)

###############################################
### Call all Libraries, including Crypto and RPLCD
##################################################

###########Define pins for LCD Display
lcd = CharLCD(numbering_mode=GPIO.BCM,cols=16,rows=2,pin_rs=4,pin_e=17,pins_data=[18,27,22,23])
lcd.clear()


##############Used to Create the main Login Window
root=Tk()
root.title('Login')
root.geometry('925x500+300+200')
root.configure(bg="#fff")
root.resizable(False,False)

   
##################Function to check username and hashed password
def signin():
   
   #########Obtain username and password entered in respective fields
    username=user.get()
    password=code.get()
   
   ####### Use SHA-256 to encode the entered "password", whether it is the correct one or not
    h=hashlib.new("SHA256")
    h.update(password.encode())
    password_hash = h.hexdigest()
       
   ############Read through saved usernames and hashed passwords in database
    file=open('datasheet.txt','r')
    d=file.read()
    r=ast.literal_eval(d)
    file.close()
   
   
   ##################Checks if username and entered hashed "password" are in the datasheet.txt file
    if username in r.keys() and password_hash == r[username]:
       
        screen=Toplevel(root)
         
        ##This is the Window to bring up the payment System
      
        screen.title("Payment System")
        screen.geometry('925x500+300+200')
        screen.config(bg="white")
        def payment():
   
            #####Obtain the entered fields for name, credit card number, 
            ##### Expiration date, and CVV code
            full_name=name.get()
            cc_num=cc.get()
            expire=exp.get()
            code=cvv.get()
           
            ####Transform each entered field into bytes
            data1 = bytes(full_name,'UTF-8')
            data2 = bytes(cc_num,'UTF-8')
            data3 = bytes(expire,'UTF-8')
            data4 = bytes(code,'UTF-8')
            
            ######Generate 16 byte Keys for each field
            key1 = get_random_bytes(16)
            key2 = get_random_bytes(16)
            key3 = get_random_bytes(16)
            key4 = get_random_bytes(16)
            
            ####Generate the Ciphertext for each field using AES CCM mode
            cipher1 = AES.new(key1, AES.MODE_CCM)
            cipher2 = AES.new(key2, AES.MODE_CCM)
            cipher3 = AES.new(key3, AES.MODE_CCM)
            cipher4 = AES.new(key4, AES.MODE_CCM)
            
            ####Take cipher bits and transform into ciphertext
            ciphertext1, tag1 = cipher1.encrypt_and_digest(data1)
            ciphertext2, tag2 = cipher2.encrypt_and_digest(data2)
            ciphertext3, tag3 = cipher3.encrypt_and_digest(data3)
            ciphertext4, tag4 = cipher4.encrypt_and_digest(data4)

            #####Print the Plaintext and Ciphertext of each field
            print('Name: %s Ciphertext: %s\n' % (data1,ciphertext1))
            print('CC Number: %s Ciphertext: %s\n' % (data2,ciphertext2))
            print('Expiration: %s Ciphertext: %s\n' % (data3,ciphertext3))
            print('CVV Code: %s Ciphertext: %s\n' % (data4,ciphertext4))
           
           
            try:
                #########Used to create a new file that saves name and encrypted
                #########Credit card number  
                file=open('record.txt','r+')
                d=file.read()
                r=ast.literal_eval(d)
               
                dict2={full_name:cc_num}
                r.update(dict2)
                file.truncate(0)
                file.close()
               
                file=open('record.txt','w')
                w=file.write(str(r))
               
               ########## Display "Payment Successful" to output window and LCD Display
                messagebox.showinfo('Confirmed','Payment Successful')
                screen.destroy()
                lcd.write_string('Payment Successful')
                time.sleep(3)
                lcd.clear()
               
               
               
            except:
               ######If record.txt file hasn't been created already
                file=open('record.txt','w')
                pp=str({'Name':'CCNum'})
                file.write(pp)
                file.close()
                   
           
               
                   
        #####Image for credit card window
        img=PhotoImage(file='cc.png')
        Label(screen,image=img,border=0,bg='white').place(x=50,y=90)

        frame = Frame(screen,width=350,height=390,bg='blue')
        frame.place(x=480,y=50)

        heading=Label(frame,text='Payment Information', fg="#57a1f8",bg='white',font=('Microsoft Yahei UI Light',14,'bold'))
        heading.place(x=60,y=5)
         
        #######Clear field prompts when user clicks on them 
        def on_enter(e):
            name.delete(0,'end')
        def on_leave(e):
            if name.get()=='':
                name.insert(0,'Name')
                  
                  
        ##############Aesthetics/Positioning Details of GUI
        name = Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft Yahei UI Light',11))
        name.place(x=30,y=60)
        name.insert(0,'Name')
        name.bind("<FocusIn>",on_enter)
        name.bind("<FocusOut>",on_leave)
        Frame(frame,width=295,height=2,bg='black').place(x=25,y=87)

         #######Clear field prompts when user clicks on them 
        def on_enter(e):
            cc.delete(0,'end')
        def on_leave(e):
            if cc.get()=='':
                cc.insert(0,'Credit Card Number')

        cc = Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft YaHei UI Light',11))
        cc.place(x=30,y=130)
        cc.insert(0,'Credit Card Number')
        cc.bind("<FocusIn>",on_enter)
        cc.bind("<FocusOut>",on_leave)
        Frame(frame,width=295,height=2,bg='black').place(x=25,y=157)

         #######Clear field prompts when user clicks on them 
        def on_enter(e):
            exp.delete(0,'end')
        def on_leave(e):
            if exp.get()=='':
                exp.insert(0,'Exp')

        exp = Entry(frame,width=10,fg='black',border=0,bg='white',font=('Microsoft YaHei UI Light',11))
        exp.place(x=30,y=200)
        exp.insert(0,'Exp')
        exp.bind("<FocusIn>",on_enter)
        exp.bind("<FocusOut>",on_leave)
        Frame(frame,width=100,height=2,bg='black').place(x=25,y=227)
         
         #######Clear field prompts when user clicks on them 
        def on_enter(e):
            cvv.delete(0,'end')
        def on_leave(e):
            if cvv.get()=='':
                cvv.insert(0,'CVV')

        cvv = Entry(frame,width=10,fg='black',border=0,bg='white',font=('Microsoft YaHei UI Light',11))
        cvv.place(x=150,y=200)
        cvv.insert(0,'CVV')
        cvv.bind("<FocusIn>",on_enter)
        cvv.bind("<FocusOut>",on_leave)
        Frame(frame,width=100,height=2,bg='black').place(x=145,y=227)



        Button(frame,width=32,pady=7,text='Submit Payment', bg='#57a1f8',fg='white',border=0,command=payment).place(x=35,y=300)

        ###########################################################
        screen.mainloop()
       
    else:
      ############This is the condition if the username and hashed password are not in database
        messagebox.showerror('Invalid','invalid username or password')
        lcd.write_string('Invalid')
        time.sleep(3)
        lcd.clear()
       
#############################################################        
def signup_command():
   
   ######### Used to Create Sign Up window
    window=Toplevel(root)
    window.title("Sign Up")
    window.geometry('925x500+300+200')
    window.configure(bg='#fff')
    window.resizable(False,False)

    def signup():
         ######## Obtain fields for username, password, and confirm password
        username=user.get()
        password=code.get()
        confirm_password=confirm_code.get()
       
        ###hash the entered password; this is the one that gets saved to database
        h=hashlib.new("SHA256")
        h.update(password.encode())
        password_hash = h.hexdigest()
       
        ###hash the entered "confirm password"; this is the one that gets saved to database
        h=hashlib.new("SHA256")
        h.update(confirm_password.encode())
        confirm_password_hash = h.hexdigest()
       
         #######Checks if "Password" and "Confirm Password" fields match
        if password_hash==confirm_password_hash:
            try:
               
                 ####Write Username and Hashed password to file called "datasheet.txt"
                file=open('datasheet.txt','r+')
                d=file.read()
                r=ast.literal_eval(d)
               
                dict2={username:password_hash}
                r.update(dict2)
                file.truncate(0)
                file.close()
               
                file=open('datasheet.txt','w')
                w=file.write(str(r))
               
               
               #####Displays "Signup Successful" to new window and LCD Display
                messagebox.showinfo('Signup','Succesfully signed up')
                lcd.write_string('Signed Up')
                time.sleep(3)
                lcd.clear()
                window.destroy()
               
            except:
               ####Creates 'datasheet.txt' if file has not been created yet
                file=open('datasheet.txt','w')
                pp=str({'Username':'password'})
                file.write(pp)
                file.close()
               
        else:
            #####Condition if hashed "Password" "Confirm Password" fields do not match
            messagebox.showerror('Invalid',"Both Passwords should match")
           
    def sign():
        window.destroy()
               
   ###Image for sign up window
    img=PhotoImage(file='park.png')
    Label(window,image=img,border=0,bg='white').place(x=50,y=90)

    frame = Frame(window,width=350,height=390,bg='blue')
    frame.place(x=480,y=50)

    heading=Label(frame,text='Sign up', fg="#57a1f8",bg='white',font=('Microsoft Yahei UI Light',23,'bold'))
    heading.place(x=100,y=5)

    def on_enter(e):
        user.delete(0,'end')
    def on_leave(e):
        if user.get()=='':
            user.insert(0,'Username')

    user = Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft Yahei UI Light',11))
    user.place(x=30,y=80)
    user.insert(0,'Username')
    user.bind("<FocusIn>",on_enter)
    user.bind("<FocusOut>",on_leave)
    Frame(frame,width=295,height=2,bg='black').place(x=25,y=107)

   #######Clear field prompts when user clicks on them 
    def on_enter(e):
        code.delete(0,'end')
    def on_leave(e):
        if code.get()=='':
            code.insert(0,'Password')

    code = Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft YaHei UI Light',11))
    code.place(x=30,y=150)
    code.insert(0,'Password')
    code.bind("<FocusIn>",on_enter)
    code.bind("<FocusOut>",on_leave)
    Frame(frame,width=295,height=2,bg='black').place(x=25,y=177)

   #######Clear field prompts when user clicks on them 
    def on_enter(e):
        confirm_code.delete(0,'end')
    def on_leave(e):
        if confirm_code.get()=='':
            confirm_code.insert(0,'Confirm Password')
            
   ##############Aesthetics/Positioning Details of GUI
    confirm_code = Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft YaHei UI Light',11))
    confirm_code.place(x=30,y=220)
    confirm_code.insert(0,'Confirm Password')
    confirm_code.bind("<FocusIn>",on_enter)
    confirm_code.bind("<FocusOut>",on_leave)
    Frame(frame,width=295,height=2,bg='black').place(x=25,y=247)



    Button(frame,width=32,pady=7,text='Sign up', bg='#57a1f8',fg='white',border=0,command=signup).place(x=35,y=280)
    label=Label(frame,text = 'I have an account',fg='black',bg='white',font=('Microsoft YaHei UI Light',9))
    label.place(x=90,y=340)

    signin=Button(frame,width=6,text='Sign in', border =0, bg='white',cursor='hand2', fg='#57a1f8',command=sign)
    signin.place(x=230,y=340)

    window.mainloop()
##############################################################        
img=PhotoImage(file='login.png')
Label(root,image=img,bg='white').place(x=50,y=50)

frame=Frame(root,width=350,height=350,bg="red")
frame.place(x=480,y=70)

heading=Label(frame,text='Sign in', fg='#57a1f8',bg='white', font=('Microsoft YaHei UI Light',23,'bold'))
heading.place(x=100,y=5)

#######Clear field prompts when user clicks on them 
def on_enter(e):
    user.delete(0,'end')
   
def on_leave(e):
        name=user.get()
        if name=='':
            user.insert(0,'Username')
           
##############Aesthetics/Positioning Details of GUI          
user= Entry(frame,width=25,fg='black',border=0,bg="white",font=('Microsoft YaHei UI Light',11))
user.place(x=30,y=80)
user.insert(0,'Username')
user.bind('<FocusIn>',on_enter)
user.bind('<FocusOut>',on_leave)
Frame(frame,width=295,height=2,bg='black').place(x=25,y=107)

def on_enter(e):
    code.delete(0,'end')
   
def on_leave(e):
        name=code.get()
        if name=='':
            code.insert(0,'Password')

code= Entry(frame,width=25,fg='black',border=0,bg="white",font=('Microsoft YaHei UI Light',11))
code.place(x=30,y=150)
code.insert(0,'Password')
code.bind('<FocusIn>',on_enter)
code.bind('<FocusOut>',on_leave)
Frame(frame,width=295,height=2,bg='black').place(x=25,y=177)



Button(frame,width=35,pady=7,text='Sign in',bg='#57a1f8',fg='white',border=0,command=signin).place(x=30,y=204)
label=Label(frame,text="Don't have an account?",fg='black',bg='white',font=('Microsoft YaHei UI Light',9))
label.place(x=60,y=270)

sign_up=Button(frame,width=6,text='Sign up', border=0,bg='white',cursor='hand2',fg='#57a1f8',command=signup_command)
sign_up.place(x=215,y=270)
root.mainloop()
