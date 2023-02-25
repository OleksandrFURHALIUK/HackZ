using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using System.Runtime.InteropServices;
using System.IO;
using System.Reflection;
using System.Runtime.CompilerServices;
//using Axzkonline;
//using System;
//using System.Collections.Generic;
//using System.Text;
using System.Diagnostics;
//using System.Runtime.InteropServices;
//using System.Reflection;
using Microsoft.CSharp;
using System.CodeDom.Compiler;
//using System.Windows.Forms;
//using System.Drawing;
//using System.Data;
//using System.ComponentModel;
//using System.Threading;
//using System.IO;

namespace plcdemo
{
    public partial class PL : Form
    {
        IntPtr h = IntPtr.Zero;
        public PL()
        {
            InitializeComponent();
        }


        //4.1  call connect function
        [DllImport("C:\\WINDOWS\\system32\\plcommpro.dll", EntryPoint = "Connect")]
        public static extern IntPtr Connect(string Parameters);
        [DllImport("plcommpro.dll", EntryPoint = "PullLastError")]
        public static extern int PullLastError();

        private void btnconnect_Click_1(object sender, EventArgs e)
        {
            string str = "";
            int ret = 0;        // Error ID number
            Cursor = Cursors.WaitCursor;

            if (this.radbtntcp.Checked)         //Obtain TCP connect options
                str = this.txttcp.Text;
            else if (this.radbtn485.Checked)
                str = this.txt485.Text;
            if (str == "")
                MessageBox.Show("Please select the connect mode:");

            if (IntPtr.Zero == h)
            {
                h = Connect(str);
                Cursor = Cursors.Default;
                if (h != IntPtr.Zero)
                {
                    MessageBox.Show("Connect device succeed!");
                    btndisconncet.Enabled = true;
                    btnconnect.Enabled = false;

                    //device param tab
                    btnselparam.Enabled = true;        //When connect device successful, The device params can be used
                    btncleparam.Enabled = true;
                    this.btngetparam.Enabled = false;
                    this.btnsetparam.Enabled = false;
                    cmbparam.Enabled = false;
                    txtchgparam.Enabled = false;
                    btnchgparam.Enabled = false;

                    //Control device tab
                    btnDevControl.Enabled = true;
                    cmbOperID.Enabled = true;
                    cmbDoorID.Enabled = false;
                    cmbOutAddr.Enabled = false;
                    txtDoorAction.Enabled = false;

                    //Device Data Tab
                    cmbdevtable.Enabled = true;
                    btngetdat.Enabled = false;
                    btnsetdat.Enabled = false;
                    btndeldata.Enabled = false;
                    btndatcount.Enabled = false;
                    btnfil.Enabled = false;
                    btnclefil.Enabled = false;
                    this.txtdevdata.Text = "\r\n \r\n Please select tablename above the frame!";

                    //RTLog Tab
                    btnrtlogstart.Enabled = true;
                    btnrtlogstop.Enabled = true;

                    //FingerPrint Tab
                    txtPin.Enabled = true;
                    txtFingerID.Enabled = true;
                    forceFPMake.Enabled = true;
                    txtTemplateDatas.Enabled = true;
                    btnRegsterFingerprint.Enabled = true;
                    btnVerifyfp.Enabled = true;
                    btnUploadFP.Enabled = true;
                    //btnDeleteFP.Enabled = true;
                }
                else
                {
                    ret = PullLastError();
                    MessageBox.Show("Connect device Failed! The error id is: " + ret);
                    btnselparam.Enabled = false;         //When disconnect device,It can not used of device params

                }

            }
        }


        //4.2 call Disconnect function
        [DllImport("plcommpro.dll", EntryPoint = "Disconnect")]
        public static extern void Disconnect(IntPtr h);


        private void btndisconncet_Click(object sender, EventArgs e)
        {
            if (IntPtr.Zero != h)
            {
                Disconnect(h);
                h = IntPtr.Zero;

                btndisconncet.Enabled = false;
                btnconnect.Enabled = true;

                //device param  tab
                btncleparam.Enabled = false;
                btnselparam.Enabled = false;
                btngetparam.Enabled = false;
                btnsetparam.Enabled = false;
                cmbparam.Enabled = false;
                txtchgparam.Enabled = false;
                btnchgparam.Enabled = false;
                lsvselparam.Items.Clear();

                //Control device tab
                btnDevControl.Enabled = false;
                cmbOperID.Enabled = false;
                cmbDoorID.Enabled = false;
                cmbOutAddr.Enabled = false;
                txtDoorAction.Enabled = false;
                cmbNorOpenOrNot.Enabled = false;
                cmbAuxoutID.Enabled = false;

                //Device Data Tab
                cmbdevtable.Enabled = false;
                btngetdat.Enabled = false;
                btnsetdat.Enabled = false;
                btndeldata.Enabled = false;
                btndatcount.Enabled = false;
                btnfil.Enabled = false;
                btnclefil.Enabled = false;

                //RTLog Tab
                btnrtlogstart.Enabled = false;
                btnrtlogstop.Enabled = false;

                //FingerPrint Tab
                txtPin.Enabled = false;
                txtFingerID.Enabled = false;
                forceFPMake.Enabled = false;
                txtTemplateDatas.Enabled = false;
                btnRegsterFingerprint.Enabled = false;
                btnVerifyfp.Enabled = false;
                btnUploadFP.Enabled = false;
                //btnDeleteFP.Enabled = false;
            }
            return;
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            this.btndisconncet.Enabled = false;
            this.cmbOperID.SelectedIndex = 1;       //The control device Operation default ID
            this.radbtntcp.Checked = true;

            //device param  tab
            this.btngetparam.Enabled = false;   //The GetParam default state is not used,When Select Device Param,It auto to change used
            btnsetparam.Enabled = false;
            btnselparam.Enabled = false;         //When disconnect device,It can not used to select device params
            btncleparam.Enabled = false;
            cmbparam.Enabled = false;
            txtchgparam.Enabled = false;
            btnchgparam.Enabled = false;

            //Control device tab
            btnDevControl.Enabled = false;
            cmbOperID.Enabled = false;
            cmbDoorID.Enabled = false;
            cmbOutAddr.Enabled = false;
            txtDoorAction.Enabled = false;

            //Device Data Tab
            cmbdevtable.Enabled = false;
            btngetdat.Enabled = false;
            btnsetdat.Enabled = false;
            btndeldata.Enabled = false;
            btndatcount.Enabled = false;
            btnfil.Enabled = false;
            btnclefil.Enabled = false;

            //RTLog Tab
            btnrtlogstart.Enabled = false;
            btnrtlogstop.Enabled = false;

            this.cmbseardev.Enabled = false;
            this.txtnewip.Enabled = false;
            //this.txtdevpwd.Enabled = false;
            this.btnmodip.Enabled = false;
        }


        //Select device param
        private void btnselparam_Click(object sender, EventArgs e)
        {
            string prestr = "";
            string selstr = "";
            bool tag = true;
            if (this.lsvpreparam.SelectedItems.Count == 0)
            {
                MessageBox.Show("Please select the params!");
                return;
            }
            else
            {
                for (int i = 0; i < this.lsvpreparam.SelectedItems.Count; i++)
                {
                    prestr = this.lsvpreparam.SelectedItems[i].Text;
                    for (int j = 0; j < this.lsvselparam.Items.Count; j++)
                    {
                        selstr = this.lsvselparam.Items[j].Text;
                        if (string.Equals(prestr, selstr))        //Remove duplicate parameters
                        {
                            tag = false;
                        }
                    }
                    if (tag)
                    {
                        this.lsvselparam.Items.Add(prestr);
                        if (this.lsvselparam.Items.Count >= (i + 1))
                        {
                            this.lsvselparam.Items[i].SubItems.Add("");
                        }
                    }
                    tag = true;
                }
                this.btngetparam.Enabled = true;
                this.btnsetparam.Enabled = true;
            }
        }


        //clean select params
        private void btncleparam_Click(object sender, EventArgs e)
        {
            if (this.lsvselparam.Items.Count == 0)
            {
                MessageBox.Show("The listview is no param!");
                return;
            }
            else
            {
                this.lsvselparam.Items.Clear();
                this.cmbparam.Items.Clear();
            }
            btngetparam.Enabled = false;
            btnsetparam.Enabled = false;
            cmbparam.Enabled = false;
            txtchgparam.Enabled = false;
            btnchgparam.Enabled = false;
        }


        //4.4 call GetDeviceParam function

        [DllImport("plcommpro.dll", EntryPoint = "GetDeviceParam")]
        public static extern int GetDeviceParam(IntPtr h, ref byte buffer, int buffersize, string itemvalues);

        private void btngetparam_Click(object sender, EventArgs e)
        {
            if (IntPtr.Zero != h)
            {
                int ret = 0, i = 0;
                int BUFFERSIZE = 10 * 1024 * 1024;
                byte[] buffer = new byte[BUFFERSIZE];
                int lv_sel_count = lsvselparam.Items.Count;
                string str = null;
                string tmp = null;
                string[] value = null;
                do
                {
                    str = str + this.lsvselparam.Items[i].Text;
                    if (i < lv_sel_count - 1)
                    {
                        str = str + ',';
                    }
                    i++;
                } while (i < lv_sel_count);
                //MessageBox.Show(str);
                ret = GetDeviceParam(h, ref buffer[0], BUFFERSIZE, str);       //obtain device's param value
                if (ret >= 0)
                {
                    tmp = Encoding.Default.GetString(buffer);
                    //MessageBox.Show(tmp);
                    value = tmp.Split(',');
                    for (int k = 0; k < lv_sel_count; k++)
                    {
                        //string sub_buf = value[k].ToString();
                        //string[] sub_str = sub_buf.Split('=');
                        string[] sub_str = value[k].Split('=');
                        if (sub_str.Length >= 2)
                        {
                            this.lsvselparam.Items[k].SubItems[1].Text = sub_str[1].ToString();
                        }
                        else
                        {
                            this.lsvselparam.Items[k].SubItems[1].Text = "";
                        }

                    }
                    //modify param value
                    cmbparam.Enabled = true;
                    txtchgparam.Enabled = true;
                    btnchgparam.Enabled = true;
                }
                else
                {
                    MessageBox.Show("GetDeviceParam function failed.The error is " + PullLastError() + ".");
                    //PullLastError();
                }
            }
            else
            {
                MessageBox.Show("Connect device failed!");
                return;
            }
        }



        //When finish modify param ,It can be used SetDeviceParam function
        private void btnchgparam_Click(object sender, EventArgs e)
        {
            for (int selcount = 0; selcount < lsvselparam.Items.Count; selcount++)
            {
                if (string.Equals(lsvselparam.Items[selcount].Text, cmbparam.SelectedItem))
                {
                    //MessageBox.Show(txtchgparam.Text);
                    this.lsvselparam.Items[selcount].SubItems[1].Text = txtchgparam.Text;     //show the modify device params
                }
            }
        }


        //It is showed params of the droplist
        private void cmbparam_DropDown(object sender, EventArgs e)
        {
            this.cmbparam.Items.Clear();
            for (int selcount = 0; selcount < lsvselparam.Items.Count; selcount++)
            {
                string selparam = lsvselparam.Items[selcount].Text;
                if (!(string.Equals(selparam, "LockCount") || string.Equals(selparam, "ReaderCount") || string.Equals(selparam, "AuxInCount") || string.Equals(selparam, "AuxOutCount") || string.Equals(selparam, "Door1CancelKeepOpenDay") || string.Equals(selparam, "Door2CancelKeepOpenDay") || string.Equals(selparam, "Door3CancelKeepOpenDay") || string.Equals(selparam, "Door4CancelKeepOpenDay")))
                {
                    this.cmbparam.Items.Add(lsvselparam.Items[selcount].Text);
                }
            }
        }


        //4.3 call SetDeviceParam function

        [DllImport("plcommpro.dll", EntryPoint = "SetDeviceParam")]
        public static extern int SetDeviceParam(IntPtr h, string itemvalues);


        private void btnsetparam_Click(object sender, EventArgs e)
        {
            int ret = 0, i = 0, tt = 0;
            string str = "";
            DateTime dt;
            do             //SetDeviceParam
            {
                if (this.lsvselparam.Items[i].SubItems.Count >= 2)
                {
                    str = str + this.lsvselparam.Items[i].Text + "=" + this.lsvselparam.Items[i].SubItems[1].Text;
                }
                else
                {
                    MessageBox.Show(this.lsvselparam.Items[i].Text + " is only read");
                }
                if (lsvselparam.Items[i].Text == "DateTime")    //Synchronization time
                {
                    dt = DateTime.Now;
                    MessageBox.Show("Now datetime is:" + dt);
                    tt = ((dt.Year - 2000) * 12 * 31 + (dt.Month - 1) * 31 + (dt.Day - 1)) * (24 * 60 * 60) + dt.Hour * 60 * 60 + dt.Minute * 60 + dt.Second;
                    MessageBox.Show("Conver now datetime is:" + tt);
                    this.lsvselparam.Items[i].SubItems[1].Text = tt.ToString();
                }
                if (i < lsvselparam.Items.Count - 1)
                {
                    str = str + ',';
                }
                i++;
            } while (i < lsvselparam.Items.Count);
            //MessageBox.Show(str);
            ret = SetDeviceParam(h, str);    //set the select param value to device
            if (ret >= 0)
                MessageBox.Show("SetDeviceParam successfu!");
            else
                PullLastError();
        }


        //4.5 call ControlDevice function

        [DllImport("plcommpro.dll", EntryPoint = "ControlDevice")]
        public static extern int ControlDevice(IntPtr h, int operationid, int param1, int param2, int param3, int param4, string options);


        private void btndevcontrol_Click(object sender, EventArgs e)
        {
            int ret = 0;
            int operID = Convert.ToInt32(this.cmbOperID.SelectedItem.ToString());
            int doorOrAuxoutID = 0;
            int outputAddrType = 0;
            int doorAction = 0;

            if (operID == 1)
            {
                outputAddrType = Convert.ToInt32(this.cmbOutAddr.SelectedItem.ToString());
                if (outputAddrType == 1)
                {
                    doorOrAuxoutID = Convert.ToInt32(this.cmbDoorID.SelectedItem.ToString());
                    doorAction = Convert.ToInt32(this.txtDoorAction.Text);
                }
                else if (outputAddrType == 2)
                {
                    doorOrAuxoutID = Convert.ToInt32(this.cmbAuxoutID.SelectedItem.ToString());
                }
               
            }
            else if (operID == 4)
            {
                doorOrAuxoutID = Convert.ToInt32(this.cmbDoorID.SelectedItem.ToString());
                outputAddrType = Convert.ToInt32(this.cmbNorOpenOrNot.SelectedItem.ToString());
            }
            if (IntPtr.Zero != h)
            {
                MessageBox.Show(operID.ToString() + "," + doorOrAuxoutID.ToString() + "," + outputAddrType.ToString() + "," + doorAction.ToString());
                ret = ControlDevice(h, operID, doorOrAuxoutID, outputAddrType, doorAction, 0, "");     //call ControlDevice funtion from PullSDK
            }
            else
            {
                MessageBox.Show("Connect device failed!The error is " + PullLastError() + " .");
                return;
            }
            if (ret >= 0)
            {
                MessageBox.Show("The operation succeed!");
                return;
            }
        }

        private void comoperid_SelectedIndexChanged(object sender, EventArgs e)
        {
            int operID = Convert.ToInt32(this.cmbOperID.SelectedItem.ToString());
            if (IntPtr.Zero != h)
            {
                int ret = 0;
                int BUFFERSIZE = 10 * 1024 * 1024;
                byte[] buffer = new byte[BUFFERSIZE];
                string items = "LockCount,AuxOutCount";
                ret = GetDeviceParam(h, ref buffer[0], BUFFERSIZE, items);
                if (ret >= 0)
                {
                    string tmp = Encoding.Default.GetString(buffer);
                    MessageBox.Show(tmp);
                    string[] value = tmp.Split(',');

                    string[] subStrLock = value[0].Split('=');
                    string[] subStrAuxout = value[1].Split('=');
                    if (subStrLock.Length == 2)
                    {
                        this.txtDoorCount.Text = subStrLock[1].ToString();
                    }
                    if (subStrAuxout.Length == 2)
                    {
                        this.txtAuxoutCount.Text = subStrAuxout[1].ToString();
                    }

                }
                else
                {
                    MessageBox.Show("Failed to get lockcount and AuxOutCount!The error is " + PullLastError() + " .");
                }

            }
            if (operID == 1)
            {
                //this.cmbdoorid.Enabled = true;

                this.cmbOutAddr.Enabled = true;
                this.cmbOutAddr.Visible = true;
                this.labelAddrType.Visible = true;
                this.labelAddrTypeValue.Visible = true;

                this.labelAuxoutID.Visible = false;
                this.cmbAuxoutID.Enabled = false;
                this.cmbAuxoutID.Visible = false;

                this.labelDoorID.Visible = false;
                this.cmbDoorID.Enabled = false;
                this.cmbDoorID.Visible = false;

                this.labelStartOrOver.Visible = false;
                this.labelStartOrOverValue.Visible = false;
                this.cmbNorOpenOrNot.Enabled = false;
                this.cmbNorOpenOrNot.Visible = false;

                this.labelDoorAction.Visible = false;
                this.labelDoorActionValue.Visible = false;
                this.txtDoorAction.Enabled = false;
                this.txtDoorAction.Visible = false;

                this.btnDevControl.Enabled = false;
                this.btnDevControl.Visible = false;
            }
            else if (operID == 4)
            {
                this.labelDoorID.Visible = true;
                this.cmbDoorID.Enabled = true;
                this.cmbDoorID.Visible = true;

                this.cmbDoorID.Items.Clear();
                int doorCount = 0;
                doorCount = Convert.ToInt32(this.txtDoorCount.Text);
                for (int i = 1; i <= doorCount; i++)
                {
                    this.cmbDoorID.Items.Add(i.ToString());
                }
                this.cmbDoorID.SelectedIndex = 0;

                this.cmbNorOpenOrNot.Visible = true;
                this.cmbNorOpenOrNot.Enabled = true;
                this.labelStartOrOver.Visible = true;
                this.labelStartOrOverValue.Visible = true;

                this.cmbOutAddr.Enabled = false;
                this.cmbOutAddr.Visible = false;
                this.labelAddrType.Visible = false;
                this.labelAddrTypeValue.Visible = false;

                this.labelAuxoutID.Visible = false;
                this.cmbAuxoutID.Enabled = false;
                this.cmbAuxoutID.Visible = false;



                this.labelDoorAction.Visible = false;
                this.labelDoorActionValue.Visible = false;
                this.txtDoorAction.Enabled = false;
                this.txtDoorAction.Visible = false;

                this.btnDevControl.Enabled = true;
                this.btnDevControl.Visible = true;
            }
            else
            {
                this.cmbNorOpenOrNot.Visible = false;
                this.cmbNorOpenOrNot.Enabled = false;
                this.labelStartOrOver.Visible = false;
                this.labelStartOrOverValue.Visible = false;

                this.cmbOutAddr.Enabled = false;
                this.cmbOutAddr.Visible = false;
                this.labelAddrType.Visible = false;
                this.labelAddrTypeValue.Visible = false;

                this.labelAuxoutID.Visible = false;
                this.cmbAuxoutID.Enabled = false;
                this.cmbAuxoutID.Visible = false;

                this.labelDoorID.Visible = false;
                this.cmbDoorID.Enabled = false;
                this.cmbDoorID.Visible = false;

                this.labelDoorAction.Visible = false;
                this.labelDoorActionValue.Visible = false;
                this.txtDoorAction.Enabled = false;
                this.txtDoorAction.Visible = false;

                this.btnDevControl.Enabled = true;
                this.btnDevControl.Visible = true;


            }
        }


        public string devtablename = "";
        private void cmbdevtable_DropDownClosed(object sender, EventArgs e)
        {
            devtablename = this.cmbdevtable.SelectedItem.ToString();
           
            if (devtablename == "")
            {
                 MessageBox.Show("Please choose a table name");
                 return;
            }
            if (string.Equals(devtablename, "user"))
            {
                this.txtdevdata.Text = "CardNo\tPin\tPassword\tGroup\tStartTime\tEndTime";
                this.cmbfil.Items.Clear();
                this.cmbfil.Items.Add("CardNo");
                this.cmbfil.Items.Add("Pin");
                this.cmbfil.Items.Add("Password");
                this.cmbfil.Items.Add("Group");
                this.cmbfil.Items.Add("StartTime");
                this.cmbfil.Items.Add("EndTime");
                this.cmbfil.SelectedIndex = 0;
                this.txtfilval.Text = "1";
            }
            else if (string.Equals(devtablename, "userauthorize"))
            {
                this.txtdevdata.Text = "Pin\tAuthorizeTimezoneId\tAuthorizeDoorId";
                this.cmbfil.Items.Clear();
                this.cmbfil.Items.Add("Pin");
                this.cmbfil.Items.Add("AuthorizeTimezoneId");
                this.cmbfil.Items.Add("AuthorizeDoorId");
                this.cmbfil.SelectedIndex = 0;
                this.txtfilval.Text = "1";
            }
            else if (string.Equals(devtablename, "holiday"))
            {
                this.txtdevdata.Text = "Holiday\tHolidayType\tLoop";
                this.cmbfil.Items.Clear();
                this.cmbfil.Items.Add("Holiday");
                this.cmbfil.Items.Add("HolidayType");
                this.cmbfil.Items.Add("Loop");
                this.cmbfil.SelectedIndex = 0;
                this.txtfilval.Text = "20110101";
            }
            else if (string.Equals(devtablename, "timezone"))
            {
                this.txtdevdata.Text = "TimezoneId\tSunTime1\tSunTime2\tSunTime3\tMonTime1\tMonTime2\tMonTime3\tTueTime1\tTueTime2\tTueTime3\tWedTime1\tWedTime2\tWedTime3\tThuTime1\tThuTime2\tThuTime3\tFriTime1\tFriTime2\tFriTime3\tSatTime1\tSatTime2\tSatTime3\tHol1Time1\tHol1Time2\tHol1Time3\tHol2Time1\tHol2Time2\tHol2Time3\tHol3Time1\tHol3Time2\tHol3Time3";
                this.cmbfil.Items.Clear();
                this.cmbfil.Items.Add("TimezoneId");
                this.cmbfil.Items.Add("SunTime1");
                this.cmbfil.Items.Add("SunTime2");
                this.cmbfil.Items.Add("SunTime3");
                this.cmbfil.Items.Add("MonTime1");
                this.cmbfil.Items.Add("MonTime2");
                this.cmbfil.Items.Add("MonTime3");
                this.cmbfil.Items.Add("TueTime1");
                this.cmbfil.Items.Add("TueTime2");
                this.cmbfil.Items.Add("TueTime3");
                this.cmbfil.Items.Add("WedTime1");
                this.cmbfil.Items.Add("WedTime2");
                this.cmbfil.Items.Add("WedTime3");
                this.cmbfil.Items.Add("ThuTime1");
                this.cmbfil.Items.Add("ThuTime2");
                this.cmbfil.Items.Add("ThuTime3");
                this.cmbfil.Items.Add("FriTime1");
                this.cmbfil.Items.Add("FriTime2");
                this.cmbfil.Items.Add("FriTime3");
                this.cmbfil.Items.Add("SatTime1");
                this.cmbfil.Items.Add("SatTime2");
                this.cmbfil.Items.Add("SatTime3");
                this.cmbfil.Items.Add("Hol1Time1");
                this.cmbfil.Items.Add("Hol1Time2");
                this.cmbfil.Items.Add("Hol1Time3");
                this.cmbfil.Items.Add("Hol2Time1");
                this.cmbfil.Items.Add("Hol2Time2");
                this.cmbfil.Items.Add("Hol2Time3");
                this.cmbfil.Items.Add("Hol3Time1");
                this.cmbfil.Items.Add("Hol3Time2");
                this.cmbfil.Items.Add("Hol3Time3");
                this.cmbfil.SelectedIndex = 0;
                this.txtfilval.Text = "1";
            }
            else if (string.Equals(devtablename, "transaction"))
            {
                this.txtdevdata.Text = "Cardno\tPin\tVerified\tDoorID\tEventType\tInOutState\tTime_second";
                this.cmbfil.Items.Clear();
                this.cmbfil.Items.Add("Cardno");
                this.cmbfil.Items.Add("Pin");
                this.cmbfil.Items.Add("Verified");
                this.cmbfil.Items.Add("DoorID");
                this.cmbfil.Items.Add("EventType");
                this.cmbfil.Items.Add("InOutState");
                this.cmbfil.Items.Add("Time_second");
                this.cmbfil.SelectedIndex = 0;
                this.txtfilval.Text = "1";
            }
            else if (string.Equals(devtablename, "firstcard"))
            {
                this.txtdevdata.Text = "Pin\tDoorID\tTimezoneID";
                this.cmbfil.Items.Clear();
                this.cmbfil.Items.Add("Pin");
                this.cmbfil.Items.Add("DoorID");
                this.cmbfil.Items.Add("TimezoneID");
                this.cmbfil.SelectedIndex = 0;
                this.txtfilval.Text = "1";
            }
            else if (string.Equals(devtablename, "multimcard"))
            {
                this.txtdevdata.Text = "Index\tDoorId\tGroup1\tGroup2\tGroup3\tGroup4\tGroup5";
                this.cmbfil.Items.Clear();
                this.cmbfil.Items.Add("Index");
                this.cmbfil.Items.Add("DoorId");
                this.cmbfil.Items.Add("Group1");
                this.cmbfil.Items.Add("Group2");
                this.cmbfil.Items.Add("Group3");
                this.cmbfil.Items.Add("Group4");
                this.cmbfil.Items.Add("Group5");
                this.cmbfil.SelectedIndex = 0;
                this.txtfilval.Text = "1";
            }
            else if (string.Equals(devtablename, "inoutfun"))
            {
                this.txtdevdata.Text = "Index\tEventType\tInAddr\tOutType\tOutAddr\tOutTime\tReserved";
                this.cmbfil.Items.Clear();
                this.cmbfil.Items.Add("Index");
                this.cmbfil.Items.Add("EventType");
                this.cmbfil.Items.Add("InAddr");
                this.cmbfil.Items.Add("OutType");
                this.cmbfil.Items.Add("OutAddr");
                this.cmbfil.Items.Add("OutTime");
                this.cmbfil.Items.Add("Reserved");
                this.cmbfil.SelectedIndex = 0;
                this.txtfilval.Text = "1";
            }
            else if (string.Equals(devtablename, "templatev10"))
            {
                this.txtdevdata.Text = "Size\tUID\tPin\tFingerID\tValid\tTemplate\tResverd\tEndTag";
                this.cmbfil.Items.Clear();
                this.cmbfil.Items.Add("Size");
                this.cmbfil.Items.Add("UID");
                this.cmbfil.Items.Add("PIN");
                this.cmbfil.Items.Add("FingerID");
                this.cmbfil.Items.Add("Valid");
                this.cmbfil.Items.Add("Template");
                this.cmbfil.Items.Add("Resverd");
                this.cmbfil.Items.Add("EndTag");
                this.cmbfil.SelectedIndex = 0;
                this.txtfilval.Text = "1";
            }

            //Device Data Tab
            cmbdevtable.Enabled = true;
            btngetdat.Enabled = true;
            btnsetdat.Enabled = true;
            btndeldata.Enabled = true;
            btndatcount.Enabled = true;
            btnfil.Enabled = true;
            btnclefil.Enabled = true;
        }


        //4.8 call GetDeviceDataCount function

        [DllImport("plcommpro.dll", EntryPoint = "GetDeviceDataCount")]
        public static extern int GetDeviceDataCount(IntPtr h, string tablename, string filter, string options);


        private void btndatcount_Click(object sender, EventArgs e)
        {
            int ret = 0;
            string options = "";
            string tablenamestr = this.cmbdevtable.SelectedItem.ToString();
            string[] count = new string[20];
            if (IntPtr.Zero != h)
            {
                MessageBox.Show("devtablename="+devtablename+",devdatfilter=" + devdatfilter+",options="+options);
                ret = GetDeviceDataCount(h, devtablename, devdatfilter, options);
                if (ret >= 0)
                {
                    //MessageBox.Show("ret=" + ret);
                    this.txtgetdata.Text = "\r\n \r\nThe " + tablenamestr + " table is : " + ret + "\r\n";
                }
            }
            else
            {
                MessageBox.Show("Connect device failed!");
                return;
            }
        }


        //4.7 call GetDeviceData function

        [DllImport("plcommpro.dll", EntryPoint = "GetDeviceData")]
        public static extern int GetDeviceData(IntPtr h, ref byte buffer, int buffersize, string tablename, string filename, string filter, string options);

        string strcount = "";

        private void btngetdat_Click(object sender, EventArgs e)
        {
            int ret = 0;
            string str = this.txtdevdata.Text;
            int BUFFERSIZE = 1 * 1024 * 1024;
            byte[] buffer = new byte[BUFFERSIZE];
            string options = "";
            bool opt = this.chkdatopt.Checked;
            if (str == "")
                this.txtdevdata.Text = "\r\n \r\n Please select tablename above the frame!";
            if (opt)
                options = "NewRecord";
            if (IntPtr.Zero != h)
            {
                //MessageBox.Show("str="+str);
                //MessageBox.Show("devdatfilter=" + devdatfilter);
                ret = GetDeviceData(h, ref buffer[0], BUFFERSIZE, devtablename, str, devdatfilter, options);
            }
            else
            {
                MessageBox.Show("Connect device failed!");
                return;
            }
            //MessageBox.Show(str);

            if (ret >= 0)
            {
                this.txtgetdata.Text = Encoding.Default.GetString(buffer);
                strcount = Encoding.Default.GetString(buffer);
                MessageBox.Show("Get " + ret + " records");
            }
            else
            {
                MessageBox.Show("Get data failed.The error is " + ret);
                return;
            }
            this.txtdevdata.Clear();
        }

        private void device_data_Click(object sender, EventArgs e)
        {

        }

        public string devdatfilter = "";
        private void btnfil_Click(object sender, EventArgs e)
        {
            if (devdatfilter == "")
            {
                this.txtfil.Clear();
                devdatfilter = this.cmbfil.SelectedItem.ToString() + "=" + this.txtfilval.Text;
                this.txtfil.Text = devdatfilter;
            }
            else
            {
                this.txtfil.Clear();
                devdatfilter = devdatfilter + "," + this.cmbfil.SelectedItem.ToString() + "=" + this.txtfilval.Text;
                this.txtfil.Text = devdatfilter;
            }
        }

        private void button1_Click_2(object sender, EventArgs e)
        {
            this.txtfil.Clear();
            devdatfilter = "";
        }


        //4.6 call SetDeviceData function

        [DllImport("plcommpro.dll", EntryPoint = "SetDeviceData")]
        public static extern int SetDeviceData(IntPtr h, string tablename, string data, string options);

        private void btnsetdat_Click(object sender, EventArgs e)
        {
            int ret = 0;
            string data = this.txtdevdata.Text;
            string options = "";
            if (data == "")
            {
                this.txtdevdata.Text = "\r\n \r\n Please input set data in here!";
                this.txtgetdata.Clear();
            }
            else
            {
                if (IntPtr.Zero != h)
                {
                    ret = SetDeviceData(h, devtablename, data, options);
                    if (ret >= 0)
                    {
                        MessageBox.Show("SetDeviceData operation succeed!");
                        return;
                    }
                    else
                        MessageBox.Show("SetDeviceData operation failed!");
                }
                else
                {
                    MessageBox.Show("Connect device failed!");
                    return;
                }
            }
        }


        //4.10 call GetRTLog function

        [DllImport("plcommpro.dll", EntryPoint = "GetRTLog")]
        public static extern int GetRTLog(IntPtr h, ref byte buffer, int buffersize);

        //public Timer t = new Timer(10000);
        private void button11_Click(object sender, EventArgs e)
        {
            trglog.Enabled = true;
            MessageBox.Show("Start to RTLog");
        }


        private void timer1_Tick(object sender, EventArgs e)        //Using real-time monitoring timer
        {
            int ret = 0, i = 0, buffersize = 256;
            string str = "";
            string[] tmp = null;
            byte[] buffer = new byte[256];
            i = this.lsvrtlog.Items.Count;          //The current list of numbers assigned to i

            if (IntPtr.Zero != h)
            {

                ret = GetRTLog(h, ref buffer[0], buffersize);
                if (ret >= 0)
                {
                    str = Encoding.Default.GetString(buffer);
                    tmp = str.Split(',');
                    //MessageBox.Show(tmp[0]);
                    this.lsvrtlog.Items.Add(tmp[0]);
                    this.lsvrtlog.Items[i].SubItems.Add(tmp[1]);
                    this.lsvrtlog.Items[i].SubItems.Add(tmp[2]);
                    this.lsvrtlog.Items[i].SubItems.Add(tmp[3]);
                    this.lsvrtlog.Items[i].SubItems.Add(tmp[4]);
                    this.lsvrtlog.Items[i].SubItems.Add(tmp[5]);
                    this.lsvrtlog.Items[i].SubItems.Add(tmp[6]);
                }
                i++;
            }
            else
            {
                MessageBox.Show("Connect device failed!");
                return;
            }
        }

        private void button10_Click(object sender, EventArgs e)
        {
            trglog.Enabled = false;
            MessageBox.Show("Stop to RTLog");
        }


        //4.11 call SearchDevice function

        [DllImport("plcommpro.dll", EntryPoint = "SearchDevice")]
        //public static extern int SearchDevice( ref byte commtype, ref byte address, ref byte buffer);
        public static extern int SearchDevice(string commtype, string address, ref byte buffer);


        private void btnseardev_Click(object sender, EventArgs e)
        {
            int ret = 0, i = 0, j = 0, k = 0;
            byte[] buffer = new byte[64 * 1024];
            string str = "";
            string[] filed = null;
            string[] tmp = null;
            string udp = "UDP";
            string adr = "255.255.255.255";

            MessageBox.Show("Start to SearchDevice!");
            this.labsearchdev.Text = "searching ......";

            ret = SearchDevice(udp, adr, ref buffer[0]);
            MessageBox.Show("ret searchdevice="+ret);
            if (ret >= 0)
            {
                int count = this.lsvseardev.Items.Count;
                if (count > 0)
                {
                    this.lsvseardev.Items.Clear();
                }
                str = Encoding.Default.GetString(buffer);
                str = str.Replace("\r\n", "\t");
                tmp = str.Split('\t');

                //int p = this.lsvseardev.Items.Count;
                while (j < tmp.Length - 1)
                {
                   
                    k = 0;
                    string[] sub_str = tmp[j].Split(',');
                    //MessageBox.Show(tmp[0]);

                    filed = sub_str[k++].Split('=');            //remove "= ",and the right value assigned to the list box 
                    this.lsvseardev.Items.Add(filed[1]);

                    filed = sub_str[k++].Split('=');
                    this.lsvseardev.Items[i].SubItems.Add(filed[1]);

                    filed = sub_str[k++].Split('=');
                    this.lsvseardev.Items[i].SubItems.Add(filed[1]);

                    filed = sub_str[k++].Split('=');
                    this.lsvseardev.Items[i].SubItems.Add(filed[1]);

                    filed = sub_str[k++].Split('=');
                    this.lsvseardev.Items[i].SubItems.Add(filed[1]);

                    i++;        //The next line of the list box
                    j++;        //The next column of each row
                }
                this.labsearchdev.Text = "";
                this.cmbseardev.Enabled = true;
                this.txtnewip.Enabled = true;
                //this.txtdevpwd.Enabled = true;
                this.btnmodip.Enabled = true;
            }
            else
            {
                MessageBox.Show("SearchDevice operation is failed!");
                return;
            }
        }

        //To achieve the drop-down box to select the device search
        private void cmbseardev_DropDown(object sender, EventArgs e)
        {
            string str = "";
            this.cmbseardev.Items.Clear();
            for (int i = 0; i < lsvseardev.Items.Count; i++)
            {
                str = this.lsvseardev.Items[i].SubItems[1].Text;
                this.cmbseardev.Items.Add(str);
            }
        }

        //Select the device to achieve the drop-down is completed, the corresponding IP address to be displayed in the text box
        private void cmbseardev_DropDownClosed(object sender, EventArgs e)
        {
            string cmbstr = "";
            string lsvstr = "";
            //if (this.cmbseardev.SelectedItem.ToString() == "")
            //cmbstr =this.cmbseardev.SelectedItem.ToString();

            if (lsvstr == "")
            {
                lsvstr = this.lsvseardev.Items[0].SubItems[1].Text;
            }
            else
            {
                lsvstr = this.cmbseardev.SelectedItem.ToString();
            }

            //MessageBox.Show(cmbstr);
            for (int i = 0; i < lsvseardev.Items.Count; i++)
            {
                lsvstr = this.lsvseardev.Items[i].SubItems[1].Text;
                if (string.Equals(cmbstr, lsvstr))
                {
                    this.txtnewip.Text = this.lsvseardev.Items[i].SubItems[1].Text;
                    break;
                }
            }
        }


        //4.12 call ModifyIPAddress function

        [DllImport("plcommpro.dll", EntryPoint = "ModifyIPAddress")]
        public static extern int ModifyIPAddress(string commtype, string address, string buffer);


        private void btnmodip_Click(object sender, EventArgs e)
        {
            int ret = 0, row = 0;
            string udp = "UDP";
            string address = "255.255.255.255";
            string buffer = "";
            string selstr = this.cmbseardev.SelectedItem.ToString();
            string itemstr = "";
            //MessageBox.Show(selstr);
            for (int i = 0; i < this.lsvseardev.Items.Count; i++)       //Which device to  modify IP address 
            {

                itemstr = this.lsvseardev.Items[i].SubItems[1].Text;
                //MessageBox.Show(itemstr);
                if (string.Equals(itemstr, selstr))
                {
                    //buffer = "MAC=" + lsvseardev.Items[i].SubItems[0].Text + "," + "IPAddress=" + txtnewip.Text + "," + "ComPwd=" + txtdevpwd.Text;
                    buffer = "MAC=" + lsvseardev.Items[i].SubItems[0].Text + "," + "IPAddress=" + txtnewip.Text;// + "ComPwd=136166";
                    row = i;
                    MessageBox.Show("ModifyIPAddress operation begin!");
                    //return;
                    ret = ModifyIPAddress(udp, address, buffer);              //call ModifyIPAddress function
                    if (ret >= 0)
                    {
                        //this.lsvseardev.Items[row].SubItems[1].Text = this.txtdevpwd.Text;
                        MessageBox.Show("ModifyIPAddress operation succeed!");
                        return;
                    }
                    else
                    { 
                        MessageBox.Show("ModifyIPAddress operation failed!"+ret);
                        return;
                    }
                }
            }

        }


        //4.15 cal GetDeviceFileData function

        [DllImport("plcommpro.dll", EntryPoint = "GetDeviceFileData")]
        public static extern int GetDeviceFileData(IntPtr h, ref byte buffer, ref int buffersize, string filename, string options);


        private void btngetdevfile_Click(object sender, EventArgs e)
        {
            int ret = 0;
            int buffersize = 4 * 1024 * 1024;
            //int[] buffersize = new int[BUFFERSIZE];
            byte[] buffer = new byte[buffersize];
            string filename = this.txtGetDevFile.Text;
            string options = "";
            string filepath = "";
            if (IntPtr.Zero != h)
            {
                if (filename == "")
                {
                    MessageBox.Show("Please input the file name!");
                }
                else
                {
                    ret = GetDeviceFileData(h, ref buffer[0], ref buffersize, filename, options);
                    if (ret >= 0)
                    {
                        SaveFileDialog saveFileDialog1 = new SaveFileDialog();
                        saveFileDialog1.Filter = "txt files(*.txt)|*.txt|All files(*.*)|*.*";
                        saveFileDialog1.FilterIndex = 2;
                        saveFileDialog1.RestoreDirectory = true;
                        saveFileDialog1.FileName = System.IO.Path.GetFileName(filename);

                        if (saveFileDialog1.ShowDialog() == DialogResult.OK)
                        {
                            filepath = saveFileDialog1.FileName;
                            FileStream fsFile = new FileStream(filepath, FileMode.Create);
                            fsFile.Seek(0, SeekOrigin.Begin);
                            fsFile.Write(buffer, 0, buffersize);
                            fsFile.Close();
                        }
                        else
                        {
                            MessageBox.Show(filename + " is not exist!");
                        }
                        MessageBox.Show("succeed download file!");
                    }
                }
            }
            else
            {
                MessageBox.Show("Handle has disconnect!");
                return;
            }
        }

        private void btntarfile_Click(object sender, EventArgs e)
        {
            string filename;
            if (this.openFileDialog1.ShowDialog() == DialogResult.OK)
            {
                filename = System.IO.Path.GetFileName(this.openFileDialog1.FileName);
                if (filename != "")
                {
                    this.txtTarFile.Text = filename;
                }
            }
        }


        //4.14 call SetDeviceFileData function

        [DllImport("plcommpro.dll", EntryPoint = "SetDeviceFileData")]
        public static extern int SetDeviceFileData(IntPtr h, string filename, ref byte buffer, int buffersize, string options);


        private void btnsetdevfile_Click(object sender, EventArgs e)
        {
            string filename = "";
            int buffersize = 0, ret = 0;
            //byte[] buffer = new byter[buffersize];
            string options = "";

            if (this.openFileDialog1.FileName == "")
            {
                MessageBox.Show("Please select file!");
                return;
            }

            FileStream fsFile = File.OpenRead(this.openFileDialog1.FileName);
            buffersize = (int)fsFile.Length;
            byte[] buffer = new byte[buffersize];

            if (fsFile.Read(buffer, 0, buffersize) != buffersize)
            {
                MessageBox.Show("Read file error!");
            }
            else
            {
                filename = this.txtTarFile.Text;

                if (IntPtr.Zero != h)
                {
                    ret = SetDeviceFileData(h, filename, ref buffer[0], buffersize, options);
                    if (ret >= 0)
                    {
                        MessageBox.Show("Uploaded file succeed!");
                        return;
                    }
                    else
                    {
                        MessageBox.Show("Uploaded file failed!error code is " + ret);
                        //ret = PullLastError();
                        return;
                    }
                    fsFile.Close();
                }
                else
                {
                    MessageBox.Show("Handle has disconnect!");
                    return;
                }
            }
        }

        private void tabControl1_Click(object sender, EventArgs e)
        {
            this.txtDoorAction.Text = "0";
            //this.cmbdevtable.SelectedIndex = 0;
            //this.txtdevdata.Text = "CardNo\tPin\tPassword\tGroup\tStartTime\tEndTime";
            //this.cmbfil.Items.Clear();
            //this.cmbfil.Items.Add("CardNo");
            //this.cmbfil.SelectedIndex = 0;
        }


        //4.9 call DeleteDeviceData function

        [DllImport("plcommpro.dll", EntryPoint = "DeleteDeviceData")]
        public static extern int DeleteDeviceData(IntPtr h, string tablename, string data, string options);


        private void btndeldata_Click(object sender, EventArgs e)
        {
            int ret = 0;
            string tablename = this.cmbdevtable.SelectedItem.ToString();
            string data = this.txtfil.Text;
            string options = "";
            if (data == "")
                this.txtdevdata.Text = "\r\n \r\n Please input delete data in here!";
            else
            {
                if (IntPtr.Zero != h)
                {
                    //MessageBox.Show("data=" + data);
                    //MessageBox.Show("options="+options);
                    ret = DeleteDeviceData(h, tablename, data, options);
                    if (ret >= 0)
                        MessageBox.Show("The deleted operation succeed!");
                    else
                        MessageBox.Show("The deleted operation failed!");
                }
            }
        }

        private void btndelall_Click(object sender, EventArgs e)
        {
            int ret = 0;
            string tablename = "";
            string data = txtdevdata.Text;
            string options = "";
            for (int i = 0; i < cmbdevtable.Items.Count; i++)
            {
                tablename = cmbdevtable.Items[i].ToString();
                if (IntPtr.Zero != h)
                {
                    ret = DeleteDeviceData(h, tablename, data, options);
                    if (ret >= 0)
                        MessageBox.Show(tablename + " Delete all operation succeed!");
                    else
                    {
                        MessageBox.Show("Delete all operation failed! " + ret);
                    }
                }
                else
                    MessageBox.Show("Please connect device");
            }
        }


        private void button1_Click(object sender, EventArgs e)
        {
            timer1.Enabled = true;

        }

        private void btnRegsterFingerprint_Click(object sender, EventArgs e)
        {
            string template = "";
            string template1 = "";
            txtTemplateDatas.Text = "";
            bool ret = false;
            int i = 0;
            axAFXOnlineMain.DefaultWindowClose = 3600;
            axAFXOnlineMain.EnrollCount = 3;

            axAFXOnlineMain.SetLanguageFile("zkonline.en");
            axAFXOnlineMain.SetVerHint = "Register fingerprint";
            axAFXOnlineMain.FPEngineVersion = "10";
            axAFXOnlineMain.IsSupportDuress = true;
            ret = axAFXOnlineMain.Register();
            if (ret)
            {
                for (i = 0; i < 10; i++)
                {
                    template = axAFXOnlineMain.GetRegFingerTemplate(i);
                    if (template != null)
                        template1 = template;
                }
                txtTemplateDatas.Text = template1;
                MessageBox.Show("Register fingerprint  succeed，?and the length of template is " + (template1.Length).ToString() + ".");
            }
            else
            {
                MessageBox.Show("Register fingerprint failed.");
                return;
            }
            return;

        }


        private void btnVerifyfp_Click(object sender, EventArgs e)
        {
            string template = "";
            bool ret = false;
            axAFXOnlineMain.SetVerHint = "Verify fingerprint";
            axAFXOnlineMain.FPEngineVersion = "10";
            ret = axAFXOnlineMain.GetVerTemplate();
            if (ret)
            {
                template = axAFXOnlineMain.VerifyTemplate;
            }
            else
            {
                MessageBox.Show("Verify fingerprint failed.");
                return;
            }
            ret = false;
            ret = axAFXOnlineMain.MatchFinger(template, txtTemplateDatas.Text);
            if (ret)
            {
                MessageBox.Show("Verify fingerprint succeed.");
            }
            else
            {
                MessageBox.Show("Verify fingerprint failed.");
                return;
            }
            return;

        }

        private void btnUploadFP_Click(object sender, EventArgs e)
        {
            //int BufferSize = 16 * 1024 * 1024;
            int ret = 0;
            //string FileName = "transaction.dat";
            string tableName = "templatev10";
            string datas = "";
            string options = "";

            Byte valid = 1;
            if (true == forceFPMake.Checked)
            {
                valid = 3;
            }

            datas = "Pin=" + txtPin.Text + "\tFingerID=" + txtFingerID.Text +
                "\tValid=" + valid.ToString() + "\tTemplate=" + txtTemplateDatas.Text;
            if (IntPtr.Zero != h)
            {
                ret = SetDeviceData(h, tableName, datas, options);

                if (0 == ret)
                {
                    MessageBox.Show("Upload fingerprint succeed");
                }
                else
                {
                    MessageBox.Show("Upload fingerprint failed.The error is：　" + ret.ToString());
                }
            }
            else
            {
                MessageBox.Show("Please connect device");
            }
        }

        private void btnDeleteFP_Click(object sender, EventArgs e)
        {
            int ret = 0;
            string tableName = "templatev10";
            string datas = "";
            string options = "";

            Byte valid = 1;
            if (true == forceFPMake.Checked)
            {
                valid = 3;
            }
            datas = "Pin=" + txtPin.Text + "\tFingerID=" + txtFingerID.Text +
                "\tValid=" + valid.ToString() + "\tTemplate=" + txtTemplateDatas.Text;
            if (IntPtr.Zero != h)
            {
                ret = DeleteDeviceData(h, tableName, datas, options);
                if (0 == ret)
                {
                    MessageBox.Show("Delete fingerprint succeed");
                }
                else
                {
                    MessageBox.Show("Delete fingerprint failed.The error is " + ret.ToString() + ".");
                }
            }
            else
            {
                MessageBox.Show("Please connect device");
            }
        }

        [DllImport("C:\\WINDOWS\\system32\\plcommpro.dll", EntryPoint = "ProcessBackupData")]
        public static extern int ProcessBackupData(byte[] data, int fileLen, ref byte Buffer, int BufferSize);



        private void btnParseDData_Click_1(object sender, EventArgs e)
        {

            //MessageBox.Show("！");
            byte[] buffer = new byte[16 * 1024 * 1024];
            byte[] buf = new byte[16 * 1024 * 1024];
            int BufferSize = 0;

            int ret = -1;

            if (this.txtTarFile.Text == "")
            {
                return;
            }
            StreamReader proFile = new StreamReader(this.openFileDialog1.FileName);
            txtSDData.AppendText("Card Number     PIN     Verify Mode     DoorID     Event   In/Out Status     Time");
            BufferSize = proFile.BaseStream.Read(buf, 0, 16 * 1024 * 1024);
            //buf = System.Text.Encoding.UTF8.GetBytes(LogStr);
            ret = ProcessBackupData(buf, BufferSize, ref buffer[0], 16 * 1024 * 1024);
            //FileStream fsFile = File.OpenRead(this.openFileDialog1.FileName);
            //BufferSize = (int)fsFile.Length;
            // byte[] FileBuf = new byte[fsFile.Length + 100];
            string strtemp = Encoding.UTF8.GetString(buffer);
            strtemp = strtemp.Replace(",", "\t");
            txtSDData.AppendText(strtemp);
            return;
        }

        private void cmboutaddr_SelectedIndexChanged(object sender, EventArgs e)
        {
            int outaddrtype = Convert.ToInt32(this.cmbOutAddr.SelectedItem.ToString());
           // MessageBox.Show(this.cmboutaddr.SelectedItem.ToString());
            if (outaddrtype == 1)//output to door
            {
                this.cmbDoorID.Items.Clear();
                int doorcount = 0;
                //MessageBox.Show(this.txtdoorcount.Text);
                doorcount = Convert.ToInt32(this.txtDoorCount.Text);
                for (int i = 1; i <= doorcount; i++)
                {
                    this.cmbDoorID.Items.Add(i.ToString());
                }
                this.cmbDoorID.SelectedIndex = 0;

                this.cmbDoorID.Enabled = true;
                this.cmbDoorID.Visible = true;
                this.labelDoorID.Visible = true;

                this.labelDoorActionValue.Visible = true;
                this.labelDoorAction.Visible = true;
                this.txtDoorAction.Enabled = true;
                this.txtDoorAction.Visible = true;

                this.cmbAuxoutID.Enabled = false;
                this.cmbAuxoutID.Visible = false;
                this.labelAuxoutID.Visible = false;

                this.btnDevControl.Enabled = true;
                this.btnDevControl.Visible = true;
            }
            else if (outaddrtype == 2)//output to auxout 
            {
                this.cmbAuxoutID.Items.Clear();
                int auxoutcount = 0;
                auxoutcount = Convert.ToInt32(this.txtAuxoutCount.Text);
                for (int i = 1; i <= auxoutcount; i++)
                {
                    this.cmbAuxoutID.Items.Add(i.ToString());
                }
                this.cmbAuxoutID.Enabled = true;
                this.cmbAuxoutID.Visible = true;
                this.labelAuxoutID.Visible = true;

                this.cmbDoorID.Enabled = false;
                this.cmbDoorID.Visible = false;
                this.labelDoorID.Visible = false;

                this.labelDoorActionValue.Visible = false;
                this.labelDoorAction.Visible = false;
                this.txtDoorAction.Enabled = false;
                this.txtDoorAction.Visible = false;

                this.btnDevControl.Enabled = true;
                this.btnDevControl.Visible = true;

            }



        }

        private void btncls_Click(object sender, EventArgs e)
        {
            this.lsvrtlog.Items.Clear();
        }

  

    }
}

