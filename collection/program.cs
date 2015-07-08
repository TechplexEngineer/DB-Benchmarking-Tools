using System;
using System.Linq;
using System.Data.SqlClient;
using System.Threading;
using System.IO;

namespace TPM_Capture
{
	public static class MyExtensions
	{
		/// <summary>
		/// Extends the DateTime object. Adds method to convert DateTime to Unix timestamp.
		/// </summary>
		/// <returns>The timesatmp.</returns>
		/// <param name="value">Value.</param>
		public static int asTimesatmp(this DateTime value)
		{
			//create Timespan by subtracting the value provided from the Unix Epoch
			TimeSpan span = (value - new DateTime(1970, 1, 1, 0, 0, 0, 0).ToLocalTime());

			//return the total seconds (which is a UNIX timestamp)
			return (int)span.TotalSeconds;
		}
	}
	class MainClass
	{
		// when to stop the benchmark read loop
		private static bool keepRunning = true;
		// when the TPS has been +/-0 this many times, stop the program
		private static int numberOfZerosBeforeQuit = 20;

		public static void Main (string[] args)
		{
			Console.WriteLine ("Starting Up");

			//create the connection
			string database = "<DB>";
			string user = "<USER>";
			string pass = "<PASS>";
			string server = "<IP>";
			
			SqlConnection myConnection = new SqlConnection("user id="+user+";" + 
				"password="+pass+";"+
				"server="+server+";" + 
				//"Trusted_Connection=yes;" + //this can be true if running on the same hist
				"database="+database+";" + 
				"connection timeout=30");
			

			using (StreamWriter w = File.AppendText("log.txt"))
			{
				try {
					myConnection.Open();
				} catch(Exception e) {
					Console.WriteLine(e.ToString());
					w.WriteLine("<<<"+e.ToString()+">>>");
					w.Flush ();
					Environment.Exit (-1);
				}


				SqlDataReader myReader = null;
				SqlCommand myCommand = new SqlCommand ("SELECT cntr_value \n\tFROM sys.dm_os_performance_counters \n\tWHERE counter_name = 'transactions/sec'\n\tAND instance_name = '"+database+"'", myConnection);

				//when the user presses ctrl+c in the console windo exit gracefully. I learned delagates are like function pointers in C
				Console.CancelKeyPress += delegate(object sender, ConsoleCancelEventArgs e) {
					e.Cancel = true;
					MainClass.keepRunning = false;
				};

				int prevTranCount = -1;
				int zeroCounter = 0;

				while (MainClass.keepRunning) {
					try {
						
						myReader = myCommand.ExecuteReader ();
						while (myReader.Read ()) { //there should only ever be one result, but this is how the example showed it working

							//the first time newTrans will be 0
							if (prevTranCount == -1)
							{
								// I wonder who thought it was a good idea to store this NUMBER as a string!
								prevTranCount = int.Parse(myReader ["cntr_value"].ToString());
								continue;
							}
							//Since TPS reported by the database is cumulative we'll subtract out the previous amount of transactions.
							int newTrans = int.Parse(myReader ["cntr_value"].ToString()) - prevTranCount;

							//this is what is logged to the file and output to the screen
							string log = String.Format("{0}\t{1}\t{2}\t{3}", DateTime.Now.asTimesatmp(), newTrans.ToString (), prevTranCount, zeroCounter);

							Console.WriteLine (log);
							w.WriteLine(log);
							prevTranCount = int.Parse(myReader ["cntr_value"].ToString());

							//if the number of newTransactions detected is less than (5) we might be done.
							if (newTrans <= 5) {
								zeroCounter ++;
							} else {
								zeroCounter = 0;
							}

							//once we've seen the requisite number of zeroes, stop the program.
							if (zeroCounter >= MainClass.numberOfZerosBeforeQuit) {
								keepRunning=false;
							}
						}
						myReader.Close();

					} catch (Exception e) {
						Console.WriteLine (e.ToString ());
						w.WriteLine("<<<"+e.ToString()+">>>");
						w.Flush ();
					}
					//there is probably a better way to delay, but this works for now.
					Thread.Sleep (1 * 1000);
				}
				w.Flush ();
			}
		}
	}
}
