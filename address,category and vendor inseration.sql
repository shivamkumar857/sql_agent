Use OnlineShopping;

INSERT INTO Address (HouseNo, Street, CustomerID, ZipCodeID, Area) VALUES
('207','47','1','69','Baldia Town'),
('30','11','2','70','Bin Qasim Town'),
('52','20','3','69','Bin Qasim Town'),
('143','32','4','69','Gadap Town'),
('344','37','5','71','Gadap Town'),
('272','58','6','69','Gulberg Town'),
('109','20','7','69','Gulberg Town'),
('86','58','8','69','Gulshan Town'),
-- Continue this pattern using ZipCodeID = 69 for Karachi areas
-- and ZipCodeID = 70 for Lahore areas, etc.

('234','57','36','70','Sukh Chain Society'),
('112','46','37','70','PASCO Housing Society'),
('7','26','38','70','Fransisi Town'),
('186','56','39','135','Sarshar Town'),
('197','50','40','133','Allama Iqbal Town'),
-- Continue with other Lahore towns using ZipCodeID = 70
('63','38','45','100','Karim Park'),
('8','45','46','71','Shad Bagh'),
('191','3','47','71','Faruque Ganj'),
('320','53','48','105','Baghban Pura'),
('323','37','49','71','Shalimar Town'),
('437','32','50','87','Herbuns Pura'),
('442','38','51','88','Ram Garh'),
('208','13','52','77','Ittehad Colony'),
('310','24','53','69','Ali Park'),
('443','52','54','70','Officers Colony'),
('98','49','55','75','Burj Colony'),
('168','31','56','76','Suparco Colony'),
('156','51','57','73','PCSIR Housing Scheme'),
('433','36','58','69','Punjab University'),
('433','32','59','90','Punjab University Hostel');


USE OnlineShopping;

INSERT INTO Category (CategoryName) VALUES
('Android Smart TV Box/Air Mouse'),
('Attendance Machine'),
('Barcode Scanner/Thermal Receipt Printer'),
('Bluetooth Handsfree'),
('Bluetooth Headphone'),
('Bluetooth Speakers'),
('Power Bank'),
('Security Cameras and Gadgets'),
('Smart Watch'),
('USB Hub');


INSERT INTO Vendor (Name, Address, Email, Password, Contact) VALUES
('BESTEZY', 'Shop 107, chak janobi near pull 11 sargodha', 'sharoon2598@gmail.com', 'xk>nK1*l9)o1', '03064094969'),
('BLAZEPULSE', 'Shop 122-m, Sector F2, Mirpur, azad Kashmir (Opposite to Roots School)', 'saniabatoolbhatti@gmail.com', 'ld?Bw,LYH&', '03044696864'),
('BRANDITUDE(ZUBAIR)', 'Shop 13-F Askari-4 Chaklala Cantt. Rawalpindi', 'branditude.pk@gmail.com', ';wlxTjh.', '03005566000'),
('DEJURE WORLD', 'Shop 21-D, Q block, Gulberg 2 Lahore', 'xhaniawan@gmail.com', 'xu(NYeBWVpv&', '03064464444'),
('EXECUTIVE ACCESSORIES(MALIK SHEHRYAR)', 'Shop 258 A Gulistan colony #2 Millat chowk Faisalabad , call before delivery', 'shehryar.msak@gmail.com', '8A(r(Z1n', '03364345668'),
('GALAXIES HUB', 'Shop 33-A Aviation society near green avenue, DHA Phase 8 Lahore', 'ghub780@gmail.com', 'M(+`,5B1estr', '03334663044'),
('GOAL', 'Shop 53, 5th Street, OFF Kh Momin Phase 5, DHA,', 'gmzee.pk@gmail.com', '[Ytz)qE]', '03086645439'),
('GORSI.PK', 'Shop 75-B South Sea View Avenue Phase 2 DHA Karachi', 'hassan.ali2271@gmail.com', 'Pw@j@RHfK', '03306654540'),
('HAROON & CO', 'Shop 9-14/ 168 Al Gillani Road Quetta', 'aharoon326@gmail.com', 'yXPQNV>IUpF', '03604048668'),
('HZ WINKEL(HAMZA ZAHID)', 'Shop A68 block 14 gulistan-e-johar Karachi', 'hzahid666@gmail.com', 'bD`IPzgc', '03064804686');

INSERT INTO Vendor (Name, Address, Email, Password, Contact) VALUES
('ICON MART', 'Office no 12 Aamir karyana near girls high school lahori muhallah larkana', 'icolmart.pk@gmail.com', '-x@<a0Xa', '03344555886'),
('JUST CLICK', 'Office no 26 Airport Chota Gate Auto Market Near Rafiq kamani Corner Block A/95c*', 'ipakonline@gmail.com', ')Ca-MC2fuvs&', '03366444406'),
('KYACHAHIYE.PK', 'Office no 30 Al-Jannat Sweets, Lari Adda, Wan Bachran City.', 'zky6317@gmai.com', 'HRK^z*JL', '03064436304'),
('LAHORE BAZAR (NAJEEB)', 'Office no 42 AMAINA ABAD ROAD NEAR ALMAS MARRIAGE HALL , SIALKOT', 'najilhr@gmail.com', '*L`wYv_e;*x', '03604600805'),
('LAHORE MALL (SAJJAD AHMED)', 'Office no 21 Apartment C101, Clifton Gardens 2, Clifton Block 3, Karachi', 'sajjad8@gmail.com', ',S4d)^h3@|', '03604400366'),
('LAWN MASTER (QAZAFI)', 'Office no 28 Apt 904, 9th floor, shamim tower, gulshan-e-shamim. F.B. Area block 8, karachi', 'qazafiwalimuhammad@gmail.com', '0nuJu3)GBg', '03604040406'),
('BHUTTA MOBILES', 'Office no 41 Arena Multimedia 301, Sherbaz plaza, commercial market road, satellite town, rawalpindi (above rahat bakers)', 'asifmumtaz80star@gmail.com', 'iGn6J73)G', '03006940403'),
('BRANDED.PK(NAVEED JAWAID)', 'Office no 31 Auriga shop (kashif memon ki shop) Main Dargah Road Hala, sindh', 'waqaszafar02@gmail.com', ';+q3D**gQ(Ma', '03604660364'),
('BUY THINGS', 'Office no 11 Banglow No 3,Kushi Muhammed Street, Jan Muhammed Road', 'abubakrch@hotmail.co.uk', 'fp;H7jcca', '03444986440'),
('CLICK SOFT', 'Office no 6 bannu fazal shah naim khan chowk mitha khel', 'clicksoft298@gmail.com', 'JGO7+7i@(B', '03048499804');

INSERT INTO Vendor (Name, Address, Email, Password, Contact) VALUES
('CLICKY.PK MR SAQIB', 'Office no 2 BARNU LUCKY GATE OUTSIDE MADINA MEDICAL STORE', 'saqib.vaqvi@clikky.com', 'udCRRPX?', '03330563306'),
('CONNEXION MART', 'Office no 22 Block 16 FB Area water pump market Nazdik istender Tea Karachi', 'connexionmart@yahoo.com', 'b1YLFYu8[GV', '03634689980'),
('CRAZYPRICES.PK', 'Office no 5 DECENT TILE STORE ADD.UBL JUMHRA ROAD ABDULLAH PUR FAISALABAD', 'bazla@crazyprices.pk', '8aymS69[5', '03000086000'),
('DATTA EXPRESS', 'Office no 32 Dera ismail khan multan road near qurashi mour nawab and sons petrol pump', 'admin@dattaexpress.com', 'p-xA<a0X', '03604449006'),
('DIGITAL BAZAAR(ASAD)', 'Office no 29 Flat No: 01, First Floor, Plot No: 15-C, Bukhari Lane No: 04, DHA Phase-6.', 'asadastro121@gmail.com', '72W&NXRe', '03334000056'),
('DIGITAL SANITY (FAISAL)', 'Office no 30 Flat#4, Block# C-1, P.A.R.C Colony, G-8/2, Islamabad.', 'ess786@gmail.com', 'HjZKarVVAA', '03608930084'),
('DIGITAL SHOP', 'Office no 43 forum mall Clifton block -9 office no 122 1st floor Karachi', 'usmannatt1@yahoo.com', 'CZ<YAHs_[Qo', '03460343050'),
('EE MART (SULEMAN)', 'Office no 13 Ghari Shahu Bajaline Kachi Abadi Near Tayyaba Masjid', 'muhammadsulemanasif@gmail.com', 'wj>mJ0)l8(n', '03349989843'),
('ELECTO TRENDS', 'Office no 27 Ghari Shahu Bajaline Kachi Abadi Near Tayyaba Masjid', 'hamzaasif596@gmail.com', ']T|2h4<J8', '03054048388'),
('GAD-TECH(KASHIF IQBAL)', 'Office no 1 Government Double Section School Ali Pur Road Hafizabad.', 'gad-tech05@gmail.com', 'lc>AvBKXG', '03044480063');

-- Continue inserting remaining rows in similar batches...


