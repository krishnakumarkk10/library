from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request
from accounts.models import LibraryRecords
from django.utils import timezone
from datetime import datetime
# Create your views here.


class CreateRecoreView(APIView):
    """
    API view to create a library record.

    This view handles the creation of a library record by accepting
    a POST request with the required fields: name, email, phone_number,
    book_name, book_author, and end_date. It validates the input data
    and creates a new record in the LibraryRecords model if the data
    is valid. If any validation fails, it returns an appropriate error
    message. If the record is created successfully, it returns a success
    message.

    Attributes:
        request (Request): The HTTP request object.

    """

    def post(self, request: Request) -> Response:
        name = request.data.get("name")
        email = request.data.get("email")
        phone_number = request.data.get("phone_number")
        book_name = request.data.get("book_name")
        book_author = request.data.get("book_author")
        end_date = request.data.get("end_date")
        if (
            not name
            or not email
            or not phone_number
            or not book_name
            or not book_author
            or not end_date
        ):
            return Response(
                {"error": "All fields are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if (
            not isinstance(name, str)
            or not isinstance(email, str)
            or not isinstance(phone_number, str)
            or not isinstance(book_name, str)
            or not isinstance(book_author, str)
            or not isinstance(end_date, str)
        ):
            return Response(
                {"error": "All fields must be strings."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if len(phone_number) != 10:
            return Response(
                {"error": "Phone number must be 10 digits."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not phone_number.isdigit():
            return Response(
                {"error": "Phone number must contain only digits."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not isinstance(end_date, str):
            return Response(
                {"error": "End date must be a string."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not end_date:
            return Response(
                {"error": "End date cannot be empty."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            LibraryRecords.objects.create(
                name=name,
                email=email,
                phone_number=phone_number,
                book_name=book_name,
                book_author=book_author,
                start_date=timezone.now(),
                end_date=datetime.strptime(end_date, "%Y-%m-%d").date(),
            )
        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {"message": "Record created successfully."},
        )


class GetRecordsView(APIView):
    """
    API view to retrieve all library records.

    This view handles the retrieval of all library records by accepting
    a GET request. It fetches all records from the LibraryRecords model
    and returns them in the response. If there are no records, it returns
    an appropriate message.

    Attributes:
        request (Request): The HTTP request object.

    """

    def get(self, request: Request) -> Response:
        records = LibraryRecords.objects.all()
        if not records:
            return Response(
                {"message": "No records found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        data = [
            {
                "id": record.id,
                "name": record.name,
                "email": record.email,
                "phone_number": record.phone_number,
                "book_name": record.book_name,
                "book_author": record.book_author,
                "start_date": record.start_date,
                "end_date": record.end_date,
            }
            for record in records
        ]
        return Response(data)


class DeleteRecordView(APIView):
    """
    API view to delete a library record.

    This view handles the deletion of a library record by accepting
    a DELETE request with the record ID. It validates the input data
    and deletes the record from the LibraryRecords model if the data
    is valid. If any validation fails, it returns an appropriate error
    message. If the record is deleted successfully, it returns a success
    message.

    Attributes:
        request (Request): The HTTP request object.
    """

    def delete(self, request: Request) -> Response:
        record_id = request.data.get("id")
        if not record_id:
            return Response(
                {"error": "Record ID is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            record = LibraryRecords.objects.get(id=record_id)
            record.delete()
        except LibraryRecords.DoesNotExist:
            return Response(
                {"error": "Record not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {"message": "Record deleted successfully."},
        )


class UpdateRecordView(APIView):
    """
    API view to update a library record.

    This view handles the update of a library record by accepting
    a PUT request with the record ID and the fields to be updated.
    It validates the input data and updates the record in the
    LibraryRecords model if the data is valid. If any validation
    fails, it returns an appropriate error message. If the record
    is updated successfully, it returns a success message.

    Attributes:
        request (Request): The HTTP request object.
    """

    def put(self, request: Request) -> Response:
        record_id = request.data.get("id")
        name = request.data.get("name")
        email = request.data.get("email")
        phone_number = request.data.get("phone_number")
        book_name = request.data.get("book_name")
        book_author = request.data.get("book_author")
        end_date = request.data.get("end_date")

        if not record_id:
            return Response(
                {"error": "Record ID is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            record = LibraryRecords.objects.get(id=record_id)
        except LibraryRecords.DoesNotExist:
            return Response(
                {"error": "Record not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if name:
            record.name = name
        if email:
            record.email = email
        if phone_number:
            record.phone_number = phone_number
        if book_name:
            record.book_name = book_name
        if book_author:
            record.book_author = book_author
        if end_date:
            record.end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        try:
            record.save()
        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {"message": "Record updated successfully."},
        )
