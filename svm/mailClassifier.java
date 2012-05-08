//import java.awt.List;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileFilter;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintStream;
import java.io.StringReader;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Map.Entry;
import java.util.List;
import java.util.Set;
import java.lang.*;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.PorterStemFilter;
import org.apache.lucene.analysis.StopAnalyzer;
import org.apache.lucene.analysis.StopFilter;
import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.en.EnglishAnalyzer;
import org.apache.lucene.analysis.snowball.SnowballAnalyzer;
import org.apache.lucene.analysis.standard.StandardTokenizer;
import org.apache.lucene.analysis.tokenattributes.TermAttribute;
import org.apache.lucene.queryParser.ParseException;
import org.apache.lucene.queryParser.QueryParser;
import org.apache.lucene.search.BooleanQuery;
import org.apache.lucene.search.Query;
import org.apache.lucene.util.Version;

//import javax.swing.text.html.HTMLDocument.Iterator;

public class mailClassifier {

	private static final String FIELD_CONTENTS = null;


	/**
	 * @param args
	 * @throws IOException 
	 * @throws ParseException 
	 */
	public static void main(String[] args) throws IOException, ParseException {
		// TODO Auto-generated method stub
		BooleanQuery.setMaxClauseCount(20000); 
		LinkedHashMap<String,Integer> lables = new LinkedHashMap<String,Integer>();
        Map<String,Collection> master = new LinkedHashMap<String,Collection>();		
		LinkedHashMap<String,Integer> frequencies=new LinkedHashMap<String,Integer>();
		LinkedHashMap<String,Integer> class2 = new LinkedHashMap<String,Integer>();
		LinkedHashMap<String,Integer> testing =new LinkedHashMap<String,Integer>();
		 Map<String,Collection> master1 = new LinkedHashMap<String,Collection>();
		 
		 Analyzer analyzers = new SnowballAnalyzer(Version.LUCENE_35,"English",StopAnalyzer.ENGLISH_STOP_WORDS_SET);
	    	QueryParser queryParser = new QueryParser(Version.LUCENE_35, FIELD_CONTENTS, analyzers);
	    	EnglishAnalyzer an = new EnglishAnalyzer(Version.LUCENE_35,StopAnalyzer.ENGLISH_STOP_WORDS_SET);
		
	    	
       
	    	
	    int cnt = 0;
		int cnt1 = 0;
		int cnt2 = 0;
		int cnt3 = 0;
		int abc = 1;
		int lable1 = 1;
		int xyz = 1;
		//String output1 = "/home/abhinav/Documents/abc/lib/training1.txt";
		String output1 = argv[0];
		System.out.println(output1);
		//String output2 = "/home/abhinav/Documents/abc/lib/testing1.txt";
		String output2 = argv[1];
		System.out.println(output2);
		//File dir = new File("/home/abhinav/Documents/proj599/trunk/test/lokay-m"); 
		File dir = new File(argv[3]); 
		
	    
	       
	    File[] subDirs = dir.listFiles(new FileFilter() {  
	        public boolean accept(File pathname) {  
	            return pathname.isDirectory();  
	        }  
	    });  
	    
	    File dirT = new File("/home/abhinav/Documents/proj599/trunk/train/lokay-m");  
	    
	    File[] subDirs1 = dirT.listFiles(new FileFilter() {  
	        public boolean accept(File pathname) {  
	            return pathname.isDirectory();  
	        }  
	    });  
	      
	    for (File subDir : subDirs) {  
	        //System.out.println(subDir.getPath());
	        String s = subDir.getPath();
	        String s1 = s.replace("/home/abhinav/Documents/proj599/dataset/", "");
	        lables.put(s1, lable1);
	        lable1++;
	    }  
		//hprint(lables);
	    
	    
	    for (File subDir : subDirs)
	    {
	    	 String s = subDir.getPath();
	    	 File dir1 = new File(s);
			 List<File> list = new ArrayList<File>();
			 getFiles1(dir1, list);
			 File[] array = (File[])list.toArray(new File[list.size()]);
			 LinkedHashMap<String,Integer> feature = new LinkedHashMap<String,Integer>();
			 feature.put("skadoosh", abc);
			 for(int j = 0;j<list.size();j++)
			  {
				 File input = new File(array[j].getAbsolutePath());
				//System.out.println(input);
				 BufferedReader reader = new BufferedReader(new FileReader ( input));
				 String line  = null;
				    StringBuilder stringBuilder = new StringBuilder();
				    String ls = System.getProperty("line.separator");
				    while( ( line = reader.readLine() ) != null )
				    {
				    	//System.out.println(line);
				    	if (line.trim().length() == 0)
				    	{
				    		cnt = cnt+1;
				    		//System.out.println("i am here");
				    	}
				    	if (cnt > 0)
				    	{
				    		stringBuilder.append( line );
				            stringBuilder.append( ls );

				    	}
				    	
				    }
				   String a=  stringBuilder.toString();
				   
				 // Here Stop word and stemming to be done .......................****** &&&&&&&&
				   
				   String resultString1 = a.replaceAll("([a-z]+)[?:!.,;]*", "$1");
			    	String resultStrin1 = resultString1.replaceAll("[^\\w ]", "");
			    	String fin1 = resultStrin1.toLowerCase();
			    	if(fin1.length()!=0)
			    		
			    	{
			    		//System.out.println(fin1);
			    		
			    		
			    		String last = removeStopWordsAndStem(fin1);
			    		String[] words1=last.split(" ");
			    		
			    	
			    	int x = hashing(words1,feature);}
				   
			  }
			 if (abc == 1)
			 {
				 first(master,feature,abc);
			 }
			 else
			 {
				 trainingprep(master,feature,abc,abc);
			 }
			 abc++;
	    }
	    master1.putAll(master);
	    //System.out.println()
	   /* ArrayList sign = (ArrayList) master1.get("skadoosh");
	    for (int i = 0;i<4;i++)
	    { System.out.println(sign.get(i));
	    
	    }*/
	    
	   writetofile(master,output1);
	  // System.out.println()
	   /* ArrayList sign = (ArrayList) master1.get("skadoosh");
	    for (int i = 0;i<4;i++)
	    { System.out.println(sign.get(i));
	    
	    }*/
	    
	    for (File subDir : subDirs1)
	    {
	    	 String s = subDir.getPath();
	    	 File dir1 = new File(s);
			 List<File> list = new ArrayList<File>();
			 getFiles1(dir1, list);
			 File[] array = (File[])list.toArray(new File[list.size()]); 
			 LinkedHashMap<String,Integer> feature = new LinkedHashMap<String,Integer>();
			 feature.put("skadoosh", xyz);
			 for(int j = 0;j<list.size();j++)
			  {
				 File input = new File(array[j].getAbsolutePath());
				//System.out.println(input);
				 BufferedReader reader = new BufferedReader(new FileReader ( input));
				 String line  = null;
				    StringBuilder stringBuilder = new StringBuilder();
				    String ls = System.getProperty("line.separator");
				    while( ( line = reader.readLine() ) != null )
				    {
				    	//System.out.println(line);
				    	if (line.trim().length() == 0)
				    	{
				    		cnt = cnt+1;
				    		//System.out.println("i am here");
				    	}
				    	if (cnt > 0)
				    	{
				    		stringBuilder.append( line );
				            stringBuilder.append( ls );

				    	}
				    	
				    }
				   String a=  stringBuilder.toString();
				   
				 // Here Stop word and stemming to be done .......................****** &&&&&&&&
				   
				   String resultString1 = a.replaceAll("([a-z]+)[?:!.,;]*", "$1");
			    	String resultStrin1 = resultString1.replaceAll("[^\\w ]", "");
			    	String fin1 = resultStrin1.toLowerCase();
			    	if(fin1.length()!=0)
			    	{
			    		
			    		String last = removeStopWordsAndStem(fin1);
			    		String[] words1=last.split(" ");
			    	
			    	int x = hashing(words1,feature);
			    	}
			 
	        }
			 testprep(master1,feature,xyz);
			 xyz++;
	    }
	   
             writetofile(master1,output2);
	}
	
///////////////////////////////////////////////////////////////////////////////////////////////////	
private static void testprep(Map<String, Collection> master1,
			LinkedHashMap<String, Integer> feature, int xyz) {
		// TODO Auto-generated method stub
	Iterator<Entry<String, Collection>> itx = master1.entrySet().iterator();
	while (itx.hasNext()) {
        Map.Entry pairs1 = (Map.Entry)itx.next();
        if(!pairs1.getKey().equals("skadoosh"))
        {
        	/*Iterator<Entry<String, Integer>> it = feature.entrySet().iterator();
        	while(it.hasNext())
        	{
        		 Map.Entry pairs = (Map.Entry)itx.next();
        		 if(pairs.getKey().equals(pairs))
        	}*/
        	if(feature.containsKey(pairs1.getKey()))
        	{
        		ArrayList values = (ArrayList) master1.get(pairs1.getKey());
        		values.add(xyz, feature.get(pairs1.getKey()));
        		master1.put((String) pairs1.getKey(), values);
        	}
        }
       //System.out.println(pairs1.getKey() + " = " + pairs1.getValue());
       //ArrayList values = (ArrayList) master1.get(pairs1.getKey());
	
	}
	
	
	}
////// **************************88 ***********************************************************************************8  ////// //
private static void writetofile1(LinkedHashMap<String, Integer> testset) throws FileNotFoundException {
		// TODO Auto-generated method stub
	FileOutputStream out1; // declare a file output object
    PrintStream p1;
    out1 = new FileOutputStream("/home/abhinav/Documents/testing.txt");
    p1 = new PrintStream( out1 );
    p1.print(testset.get("sign"));
    testset.remove("sign");
    Iterator<Entry<String, Integer>> it = testset.entrySet().iterator();
	int a = 1;
    while(it.hasNext())
    {
    	Map.Entry pairs = (Map.Entry)it.next();
		String s = (String) pairs.getKey();
		p1.print(" "+a+":"+testset.get(s));
		a++;
		
    }
		
	}


private static void getFiles1(File folder1, List<File> list1) {
    folder1.setReadOnly();
    File[] files1 = folder1.listFiles();
    for(int i = 0; i < files1.length; i++) {
        list1.add(files1[i]);
        if(files1[i].isDirectory())
            getFiles1(files1[i], list1);
    }
}


private static LinkedHashMap<String, Integer> testingprep(Map<String, Collection> master,
			LinkedHashMap<String, Integer> testing) {
	
	LinkedHashMap<String,Integer> ret =new LinkedHashMap<String,Integer>();
    Iterator<Entry<String, Collection>> it = master.entrySet().iterator();
    ret.put("sign",0);
    while(it.hasNext())
    {
    	Map.Entry pairs = (Map.Entry)it.next();
		String s = (String) pairs.getKey();
		if(testing.containsKey(s))
		{
			ret.put(s, testing.get(s));
			
		}
		else
		{
			ret.put(s, 0);
		}
	
    }
	
				return ret;
		// TODO Auto-generated method stub
		
	}
private static void writetofile(Map<String, Collection> master, String outputfile) throws FileNotFoundException {
		// TODO Auto-generated method stub
	FileOutputStream out1; // declare a file output object
    PrintStream p1;
    //System.out.println("Size of master   "+master.size());
    out1 = new FileOutputStream(outputfile);
    p1 = new PrintStream( out1 );
    ArrayList sign = (ArrayList) master.get("skadoosh");
    master.remove("skadoosh");
    int x = sign.size();
    for (int i = 0;i< x;i++)
    {
    	int a = 1;
    	 Iterator it = master.entrySet().iterator();
    	 p1.print(sign.get(i));
	     while (it.hasNext()) 
	     {
	           Map.Entry pairs = (Map.Entry)it.next();
	           //p1.print(index + ":" + pairs2.getValue()+ " ");
	           ArrayList values = (ArrayList) master.get(pairs.getKey());
	           int z = (Integer) values.get(i);
	          // p1.print(sign.get(i));
	           if(z !=0)
	           {
	           p1.print(" "+a+":"+z+" ");
	           }
	           a++;
	     }
	    p1.print("\n");
	           
    	
    }
    
    
	}


private static void first(Map<String, Collection> master,
			LinkedHashMap<String, Integer> frequencies, int abc) {
		// TODO Auto-generated method stub
	Iterator<Entry<String, Integer>> it = frequencies.entrySet().iterator();
	/*Collection values1 = new ArrayList();
    master.put("sign",values1);
    values1.add(abc);*/
	while(it.hasNext())
	{
		Map.Entry pairs4 = (Map.Entry)it.next();
		String s = (String)pairs4.getKey();
		int v = frequencies.get(s);
		Collection values = new ArrayList();
	    master.put(s,values);
	    values.add(v);
		//master.put(s, value)
	    
		
	}
	//System.out.println(master.get("xx"));
		//hprint1(master);
	}

private static void hprint1(Map<String, Collection> master) {
	// TODO Auto-generated method stub
	Iterator<Entry<String, Collection>> itx = master.entrySet().iterator();
	while (itx.hasNext()) {
        Map.Entry pairs1 = (Map.Entry)itx.next();
       System.out.println(pairs1.getKey() + " = " + pairs1.getValue());
       ArrayList values = (ArrayList) master.get(pairs1.getKey());
       //System.out.println(values.get(0));
       
       // itx.remove(); // avoids a ConcurrentModificationException
    }
	//System.out.println("**********************");
	
}


private static void trainingprep(Map<String, Collection> master,
			LinkedHashMap<String, Integer> frequencies, int sign, int num) {
		// TODO Auto-generated method stub
	//System.out.println(master.get("sign"));
	Iterator<Entry<String, Collection>> it = master.entrySet().iterator();
	
    while(it.hasNext())
    {
    	Map.Entry pairs = (Map.Entry)it.next();
		String s = (String) pairs.getKey();
		if(frequencies.containsKey(s))
		{
			//System.out.println(s);
			//System.out.println(master.get(s));
			//Collection value3 = new ArrayList();
			 Collection value3 = master.get(s);
			
			value3.add(frequencies.get(s));
			master.put(s, value3);
			//System.out.println(master.get(s));
			frequencies.remove(s);
		}
		else
		{
			Collection value4 = master.get(s);
			master.put(s, value4);
			value4.add(0);
			
		}
    	
    }
    Iterator<Entry<String, Integer>> it1 = frequencies.entrySet().iterator();
    while(it1.hasNext())
    {
    	Map.Entry pairs1 = (Map.Entry)it1.next();
		String s1 = (String) pairs1.getKey();
		
		Collection value1 = new ArrayList();
		master.put(s1, value1);
		for (int i = 0; i < num -1;i++)
		{
			value1.add(0);
		}
		value1.add(frequencies.get(s1));
    
    }
	
		
	}




public static int hashing(String Words[], HashMap<String, Integer> frequencies)
    
    {
    	// HashMap<String,Integer> frequencies1=new HashMap<String,Integer>();
    	
    	for (String w: Arrays.asList(Words)){
      	  Integer num=frequencies.get(w);
      	  if (num!=null)
      	    frequencies.put(w,num+1);
      	  else
      	    frequencies.put(w,1);
      	  
            
    	 }
    	
    	return 1;
    	
    }


public static void hprint(LinkedHashMap<String, Integer> a)
{
	Iterator<Entry<String, Integer>> itx = a.entrySet().iterator();
	while (itx.hasNext()) {
        Map.Entry pairs1 = (Map.Entry)itx.next();
       System.out.println(pairs1.getKey() + " = " + pairs1.getValue());
       // itx.remove(); // avoids a ConcurrentModificationException
    }
	System.out.println("**********************");
}
public static String removeStopWordsAndStem(String input) throws IOException {
    /*Set<String> stopWords = new HashSet<String>();
    stopWords.add("a");
    stopWords.add("I");
    stopWords.add("the");*/
	String[] stopWords = new String[]{"a", "about", "above", "above", "across", "after", "afterwards", "again",
    		"against", "all", "almost", "alone", "along", "already", "also","although","always","am","among",
    		"amongst", "amoungst", "amount", "an", "and", "another", "any","anyhow","anyone","anything","anyway",
    		"anywhere", "are", "around", "as", "at", "back","be","became", "because","become","becomes", "becoming", "been",
    		"before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", 
    		"bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe",
    		"detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere",
    		"empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", 
    		"fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four",
    		"from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here",
    		"hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred"
    		, "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", 
    		"latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", 
    		"moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", 
    		"nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of",
    		"off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours",
    		"ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", 
    		"seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", 
    		"six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still",
    		"such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there",
    		"thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this",
    		"those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", 
    		"towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", 
    		"well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby",
    		"wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom",
    		"whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself",
    		"yourselves", "the"};
	 List<String> list = Arrays.asList(stopWords);
	    Set<String> set = new HashSet<String>(list);

	    
    	
    

    TokenStream tokenStream = new StandardTokenizer(Version.LUCENE_35, new StringReader(input));
    tokenStream = new StopFilter(true, tokenStream, set);
    tokenStream = new PorterStemFilter(tokenStream);

    StringBuilder sb = new StringBuilder();
    TermAttribute termAttr = tokenStream.getAttribute(TermAttribute.class);
    while (tokenStream.incrementToken()) {
        if (sb.length() > 0) {
            sb.append(" ");
        }
        sb.append(termAttr.term());
    }
    return sb.toString();
}

	


}
